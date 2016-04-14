#!/usr/bin/python
# coding: utf-8
import os
import sys
import xlrd
from export_xls import configs
import slpp

#
convert_value_type = {
    int: 1,
    float: 2,
    str: 3,
    }

s = slpp.SLPP()


def load_config(config_file_name):
    try:
        with open(config_file_name, 'r') as f:
            data = f.read()
            _, data = data.split("=", 1)
            return s.decode(data)
    except IOError:
        return {}


def convert(configname, argv, excel_dir, out_lua_dir, currSliceConfig):
    xls_file_name = os.path.join(excel_dir, argv['fileName'] + '.xls')
    print u'处理', configname

    # 打开 excel
    xls = xlrd.open_workbook(xls_file_name)
    sheet = xls.sheet_by_name(argv['sheetName'])

    # 导出的 lua 文件名
    config_file_name = os.path.join(out_lua_dir, configname + '.lua')

    # 生成新的 lua 文件
    lua = open(config_file_name, 'w+')
    lua.write('--./config/%s.lua\n\n' % configname)
    lua.write('%s = {\n' % configname)

    # 要导出的列
    export_col = {}
    configkey2sheetcol = {}
    for config_key_name, config_argv in argv['readOnlyCol'].items():
        # init
        export_col[config_argv['colName']] = None
        configkey2sheetcol[config_key_name] = config_argv['colName']

    for col in range(sheet.ncols):
        v = sheet.cell_value(1, col)
        if isinstance(v, unicode) and (v in export_col):
            export_col[v] = col

        if isinstance(v, unicode) and v == argv['primeKey']:
            export_col[v] = col

    # export config
    for row in range(2, sheet.nrows):
        # table key
        cell_value = sheet.cell_value(row, export_col[argv['primeKey']])  # maybe use getDefault better
        keyID = int(cell_value)

        # 当前导出数据行
        curr_data = {}
        for config_key_name, config_argv in argv['readOnlyCol'].items():
            # print 'row : %d'%row, config_argv['colName']
            curr_data[config_key_name] = sheet.cell_value(row, export_col[config_argv['colName']])  # value

        if ('sliceKey' in argv) and not currSliceConfig['sliceFunc'](curr_data[argv['sliceKey']]):
            continue

        for config_key_name, config_argv in argv['readOnlyCol'].items():
            if ('invalid' in config_argv) and config_argv['invalid'](curr_data[config_key_name]):
                # 无效项
                curr_data[config_key_name] = None
                if ('ignore' in config_argv):
                    # 检查忽略项
                    for ignore_key in config_argv['ignore']:
                        curr_data[ignore_key] = None

        # for config_key_name, value in curr_data.items():
        # 按配置表列序输出
        # print '------ export_col ------'
        # for k, v in export_col.items():
        #     print k, ' = ', v

        # print '------ c2s ------'
        # for k, v in configkey2sheetcol.items():
        #     print k, ' = ', v

        # print '------ curr_data ------'
        # for k, v in curr_data.items():
        #     print k, ' = ', v

        lua.write('\t[%d] = {\n' % keyID)
        for config_key_name, value in sorted(curr_data.items(), key=lambda d: export_col[configkey2sheetcol[d[0]]]):
            if value is not None:
                if isinstance(value, unicode):
                    value = value.encode('utf-8')
                try:
                    value = argv['readOnlyCol'][config_key_name]['convert'](value)
                except Exception:
                    print '---- 导出异常 ----'
                    print '    config_name = ' + argv['fileName']
                    print 'config_key_name = ' + argv['readOnlyCol'][config_key_name]['colName']
                    print '     origin_row = ' + str(row)
                    print '     origin_col = ' + str(export_col[argv['readOnlyCol'][config_key_name]['colName']])
                    print '   origin_value = ' + str(value)
                    sys.exit(0)

                if 'check' in argv['readOnlyCol'][config_key_name]:
                    argv['readOnlyCol'][config_key_name]['check'](value, argv['fileName'], argv['sheetName'], argv['readOnlyCol'][config_key_name]['colName'], row)

                if isinstance(value, str):
                    lua.write('\t\t%s = "%s",\n' % (config_key_name, str(value)))
                else:
                    lua.write('\t\t%s = %s,\n' % (config_key_name, str(value)))
        lua.write('\t},\n')

    lua.write('}\n\n\n')

    lua.close()


def main(excel_dir, out_lua_dir):
    for configname, argv in configs.items():
        if 'sliceKey' in argv:
            print '处理分片: ', configname
            checkSliceNameLink = ''
            allSlicesStr = ''
            for _slicename, currSliceConfig in argv['sliceConfig'].items():
                sliceconfigname = configname + '_' + _slicename
                checkSliceNameLink += '%s[k] or ' % sliceconfigname
                allSlicesStr += (sliceconfigname + ',\n\t\t')
                convert(sliceconfigname, argv, excel_dir, out_lua_dir, currSliceConfig)

            config_file_name = os.path.join(out_lua_dir, configname + '.lua')
            lua = open(config_file_name, 'w+')
            lua.write('--./config/%s.lua\n\n' % configname)
            lua.write('%s = {}\n' % configname)
            lua.write('setmetatable(%s, {__index = function(t, k)return %s end})\n' % (configname, checkSliceNameLink + ' nil'))
            lua.write('function %s:getAllSlices() return { %s } end''' % (configname, allSlicesStr))
            lua.close()
        else:
            convert(configname, argv, excel_dir, out_lua_dir, None)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main('../', sys.argv[1])
    else:
        main('../', '../../win32_client/config/')
