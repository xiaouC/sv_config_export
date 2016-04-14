# coding: utf-8


"""
配置导出脚本：
ver: 20140619



导出脚本说明：

关键词:
fileName,    配置表.xls文件名, 建议时英文文件名
sheetName,   配置表表名, 导出的表名前被默认添加前缀'export-'
primeKey,    导出主键名,
sliceKey,    切片列-只支持被导出的列, 被导出后，在原configname table中会有如下方法: getAllSlices
sliceConfig, 切片规则 {name : {sliceFun, }}
readOnlyCol, 直接读取的列数据,
    colName,     列名, 须以unicode编码，建议英文
    convert,     类型转换方法, 支持python内建的转换方法，int, str, float, long, ...
    invalid,     无效的值, lambda x : [bool expression]
    ignore,      忽略的导出键, list类型，内容为exported_table_key的枚举
    check,       校验方法
functionCol, 支持的公式配置,内容为lua代码的文本字符串



'EXPORTED_CONFIG_TABLE_NAME' : \
        {
            'fileName'   : u'.xls file name',
            'sheetName'  : u'sheet name',
            'primeKey'   : u'col name',
            'readOnlyCol': \
                {
                    'exported_table_key' : {'colName' : u'col name',    'convert' : pythonFunc,    ['invalid' : invalid value,    'ignore' : [ignore table key enum]]},
                    ...
                },
            ['functionCol': \
                {
                    'exported_table_key' : ''' lua code '''
                },]
        },
"""

import json

def checkJsonStr(value, filename, sheetname, colname, row):
    try:
        json.loads(value)
    except Exception:
        print '---------------------------------------'
        print '-          JSON FORMAT ERROR          -'
        print '-   file: ', filename
        print '-  sheet: ', sheetname
        print '-    col: ', colname
        print '-    raw: ', row
        print '---------------------------------------'
        exit(0)


def covertStr(value):
    string = str(value)
    string.replace( "\"", "\\\"" )
    return string




configs = \
    {
        #'C_UNITS_TEST' : \
        #    {
        #        'fileName'   : u'Actor_Config',
        #        'sheetName'  : u'Lvup',
        #        'primeKey'   : u'lv',
        #        'readOnlyCol': \
        #            {
        #                'exp'   : {'colName': u'exp',   'convert' : int, 'invalid' : 10, 'ignore' : ['sp']},
        #                'power' : {'colName': u'power', 'convert' : int, 'invalid' : -1.0},
        #                'sp'    : {'colName': u'sp',    'convert' : int, 'invalid' : -1.0},
        #            },
        #        'functionCol': \
        #            {
        #                'price' : '''
        #                         function(config)
        #                             return config.exp + config.power + config.sp
        #                         end'''
        #            },
        #    },


        'C_INITPLAYER' : \
            {
                'fileName'   : u'CreatePlayer',
                'sheetName'  : u'client-initPlayer',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'prototypeID'  : {'colName' : u'prototypeID', 'convert' : int },
                        'bodyID'       : {'colName' : u'bodyID',      'convert' : int },
                    },
            },

        'C_UNITS' : \
            {
                'fileName'   : u'units',
                'sheetName'  : u'export-units',
                'primeKey'   : u'id',
                'sliceKey'   : u'class', #导出的名字
                'sliceConfig': {
                        'class0'  : {'sliceFunc': lambda x: x == 0.0},
                        'class1'  : {'sliceFunc': lambda x: x == 1.0},
                        'class2'  : {'sliceFunc': lambda x: x == 2.0},
                        'class3'  : {'sliceFunc': lambda x: x == 3.0},
                        'class4'  : {'sliceFunc': lambda x: x == 4.0},
                        'class5'  : {'sliceFunc': lambda x: x > 4.0},
                    },
                'increment'  : True,
                'readOnlyCol': \
                    {
                        #当前不导出name列，采用公式属性索引SAME_UNITS表，若出现需要同same但不同明，如孙悟空、齐天大圣、斗战胜佛，则导出_name，在公式属性中优先索引当前_name再索引SAME_UNITS表
                        #'_name'                  : {'colName' : u'name',                 'convert' : covertStr },
                        #'name'                  : {'colName' : u'name',                 'convert' : covertStr },
                        'same'                  : {'colName' : u'same',                 'convert' : int },
                        'size'                  : {'colName' : u'size',                 'convert' : int },
                        'attr'                  : {'colName' : u'attr',                 'convert' : int },
                        'mtype'                 : {'colName' : u'mtype',                'convert' : int },
                        'ability'               : {'colName' : u'ability',              'convert' : int },
                        'mvRgeTL'               : {'colName' : u'mvRgeTL',              'convert' : int },
                        'mvRgeT'                : {'colName' : u'mvRgeT',               'convert' : int },
                        'mvRgeTR'               : {'colName' : u'mvRgeTR',              'convert' : int },
                        'mvRgeL'                : {'colName' : u'mvRgeL',               'convert' : int },
                        'mvRgeR'                : {'colName' : u'mvRgeR',               'convert' : int },
                        'mvRgeBL'               : {'colName' : u'mvRgeBL',              'convert' : int },
                        'mvRgeB'                : {'colName' : u'mvRgeB',               'convert' : int },
                        'mvRgeBR'               : {'colName' : u'mvRgeBR',              'convert' : int },
                        #'evoStep'               : {'colName' : u'evoStep',              'convert' : int },
                        #'lvMax'                 : {'colName' : u'lvMax',                'convert' : int },
                        'hpMin'                 : {'colName' : u'hpMin',                'convert' : int },
                        'hpMax'                 : {'colName' : u'hpMax',                'convert' : int },
                        'atkMin'                : {'colName' : u'atkMin',               'convert' : int },
                        'atkMax'                : {'colName' : u'atkMax',               'convert' : int },
                        'defMin'                : {'colName' : u'defMin',               'convert' : int },
                        'defMax'                : {'colName' : u'defMax',               'convert' : int },
                        'critMin'               : {'colName' : u'critmin',              'convert' : int },
                        'dodgeMin'              : {'colName' : u'dodgemin',             'convert' : int },
                        'rarity'                : {'colName' : u'rarity',               'convert' : int },
                        #'evoProc'               : {'colName' : u'herostep',             'convert' : int },
                        'cexp'                  : {'colName' : u'cexp',                 'convert' : float},
                        'gtype'                 : {'colName' : u'gtype',                'convert' : int },
                        #'cost'                  : {'colName' : u'cost',                 'convert' : int },
                        'mexp'                  : {'colName' : u'mexp',                 'convert' : int },
                        #'sellk'                 : {'colName' : u'sellk',                'convert' : int },
                        #'skill'                 : {'colName' : u'skill',                'convert' : int },
                        #'lSkill'                : {'colName' : u'lSkill',               'convert' : int },
                        'seq'                   : {'colName' : u'seq',                  'convert' : int },
                        'gupm'                  : {'colName' : u'gupm',                 'convert' : int },
                        'gupr'                  : {'colName' : u'gupr',                 'convert' : int },
                        'gup1'                  : {'colName' : u'gup1',                 'convert' : int },
                        'gupType1'              : {'colName' : u'guptype1',             'convert' : int },
                        'gupnum1'               : {'colName' : u'gupnum1',              'convert' : int },
                        'gup2'                  : {'colName' : u'gup2',                 'convert' : int },
                        'gupType2'              : {'colName' : u'guptype2',             'convert' : int },
                        'gupnum2'               : {'colName' : u'gupnum2',              'convert' : int },
                        'gup3'                  : {'colName' : u'gup3',                 'convert' : int },
                        'gupType3'              : {'colName' : u'guptype3',             'convert' : int },
                        'gupnum3'               : {'colName' : u'gupnum3',              'convert' : int },
                        'gup4'                  : {'colName' : u'gup4',                 'convert' : int },
                        'gupType4'              : {'colName' : u'guptype4',             'convert' : int },
                        'gupnum4'               : {'colName' : u'gupnum4',              'convert' : int },
                        'eMaxLv'                : {'colName' : u'eMaxLv',               'convert' : int },
                        'eHpMin'                : {'colName' : u'eHpMin',               'convert' : int },
                        'eHpMax'                : {'colName' : u'eHpMax',               'convert' : int },
                        'eAtkMin'               : {'colName' : u'eAtkMin',              'convert' : int },
                        'eAtkMax'               : {'colName' : u'eAtkMax',              'convert' : int },
                        'eDefMin'               : {'colName' : u'eDefMin',              'convert' : int },
                        'eDefMax'               : {'colName' : u'eDefMax',              'convert' : int },
                        'eCritMin'              : {'colName' : u'ecritmin',             'convert' : int },
                        'eDodgeMin'             : {'colName' : u'edodgemin',            'convert' : int },
                        'coinUp'                : {'colName' : u'coinUp',               'convert' : int },
                        'expUp'                 : {'colName' : u'expUp',                'convert' : int },
                        #'dir'                   : {'colName' : u'dir',                  'convert' : int },
                        #'bfY'                   : {'colName' : u'bfY',                  'convert' : int },
                        #'model'                 : {'colName' : u'model',                'convert' : int },
                        #'origin'                : {'colName' : u'origin',               'convert' : covertStr , 'invalid' : lambda x: x == 0.0},
                        'step'                  : {'colName' : u'step',                 'convert' : int },
                        #'unitsdesc'             : {'colName' : u'unitsdesc',            'convert' : covertStr },
                        'piece_amount'          : {'colName' : u'piece_amount',         'convert' : int },
                        'hpUnit'                : {'colName' : u'mhp',                  'convert' : int },
                        'atkUnit'               : {'colName' : u'matk',                 'convert' : int },
                        'defUnit'               : {'colName' : u'mdef',                 'convert' : int },
                        'critUnit'              : {'colName' : u'mcrit',                'convert' : int },
                        'dodgeUnit'             : {'colName' : u'mdodge',               'convert' : int },
                        'breakThroughLevelMax'  : {'colName' : u'breakLv',              'convert' : int },
                        'breakThroughMatrlID'   : {'colName' : u'cid',                  'convert' : int },
                        'breakThroughMatrlCnt'  : {'colName' : u'camount',              'convert' : int },
                        'eHpUnit'               : {'colName' : u'emhp',                 'convert' : int },
                        'eAtkUnit'              : {'colName' : u'ematk',                'convert' : int },
                        'eDefUnit'              : {'colName' : u'emdef',                'convert' : int },
                        'eCritUnit'             : {'colName' : u'emcrit',               'convert' : int },
                        'eDodgeUnit'            : {'colName' : u'emdodge',              'convert' : int },
                        'skillsTree'            : {'colName' : u'skills',               'convert' : int },
                        'init_equip'            : {'colName' : u'equip',                'convert' : covertStr },
                        'excl_equip'            : {'colName' : u'excl_equip',           'convert' : int },
                        'skill1_base_power'     : {'colName' : u'skill_base1',          'convert' : int },
                        'skill2_base_power'     : {'colName' : u'skill_base2',          'convert' : int },
                        'skill3_base_power'     : {'colName' : u'skill_base3',          'convert' : int },
                        'skill4_base_power'     : {'colName' : u'skill_base4',          'convert' : int },
                        'skill5_base_power'     : {'colName' : u'skill_base5',          'convert' : int },
                        'skill1_addition'       : {'colName' : u'skill_lvup1',          'convert' : int },
                        'skill2_addition'       : {'colName' : u'skill_lvup2',          'convert' : int },
                        'skill3_addition'       : {'colName' : u'skill_lvup3',          'convert' : int },
                        'skill4_addition'       : {'colName' : u'skill_lvup4',          'convert' : int },
                        'skill5_addition'       : {'colName' : u'skill_lvup5',          'convert' : int },
                        #'skill1'                : {'colName' : u'new_skill1',           'convert' : int },
                        #'skillAvailLimit1'      : {'colName' : u'skill_open_step1',     'convert' : int },
                        #'skill2'                : {'colName' : u'new_skill2',           'convert' : int },
                        #'skillAvailLimit2'      : {'colName' : u'skill_open_step2',     'convert' : int },
                        #'skill3'                : {'colName' : u'new_skill3',           'convert' : int },
                        #'skillAvailLimit3'      : {'colName' : u'skill_open_step3',     'convert' : int },
                        'class'                 : {'colName' : u'class',                'convert' : int, 'invalid' : lambda x: x == 0.0},
                        'sound'                 : {'colName' : u'sound',                'convert' : int, 'invalid' : lambda x: x == 0.0},
                        'fightsound'            : {'colName' : u'fightsound',           'convert' : int, 'invalid' : lambda x: x == 0.0},
                        'break_addition_hp'     : {'colName' : u'hp_break',             'convert' : covertStr },
                        'break_addition_atk'    : {'colName' : u'atk_break',            'convert' : covertStr },
                        'break_addition_def'    : {'colName' : u'def_break',            'convert' : covertStr },
                    },
                #'functionCol': \
                #    {
                #        'name'       : '''function(config, key) return C_UNITS_SAME[config.same] and C_UNITS_SAME[config.same].name or "" end''',
                #        'unitsdesc'  : '''function(config, key) return C_UNITS_SAME[config.same] and C_UNITS_SAME[config.same].unitsdesc or "" end''',
                #        'sound'      : '''function(config, key) return C_UNITS_SAME[config.same] and C_UNITS_SAME[config.same].sound or 0 end''',
                #        'fightsound' : '''function(config, key) return C_UNITS_SAME[config.same] and C_UNITS_SAME[config.same].fightsound or 0 end''',
                #    },
            },

        'C_UNITS_SAME' : \
            {
                'fileName'   : u'units',
                'sheetName'  : u'client-same_units',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'name'                  : {'colName' : u'name',                 'convert' : covertStr },
                        'unitsdesc'             : {'colName' : u'unitsdesc',            'convert' : covertStr },
                        'sound'                 : {'colName' : u'sound',                'convert' : int, 'invalid' : lambda x: x == 0.0},
                        'fightsound'            : {'colName' : u'fightsound',           'convert' : int, 'invalid' : lambda x: x == 0.0},

                        'name1'                 : {'colName' : u'name1',                'convert' : covertStr },
                        'name2'                 : {'colName' : u'name2',                'convert' : covertStr },
                        'name3'                 : {'colName' : u'name3',                'convert' : covertStr },
                        'desc1'                 : {'colName' : u'desc1',                'convert' : covertStr },
                        'desc2'                 : {'colName' : u'desc2',                'convert' : covertStr },
                        'desc3'                 : {'colName' : u'desc3',                'convert' : covertStr },
                        'model1'                : {'colName' : u'model1',               'convert' : int },
                        'model2'                : {'colName' : u'model2',               'convert' : int },
                        'model3'                : {'colName' : u'model3',               'convert' : int },
                        'quality'               : {'colName' : u'quality',              'convert' : int },
                        'recommend_atk'         : {'colName' : u'position_atk',         'convert' : int },
                        'recommend_def'         : {'colName' : u'position_def',         'convert' : int },
                    },
            },

        'C_SKILLS_TREE' : \
            {
                'fileName'   : u'units',
                'sheetName'  : u'client-skills',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'skill1'                : {'colName' : u'new_skill1',           'convert' : int },
                        'skillAvailLimit1'      : {'colName' : u'skill_open_step1',     'convert' : int },
                        'skill2'                : {'colName' : u'new_skill2',           'convert' : int },
                        'skillAvailLimit2'      : {'colName' : u'skill_open_step2',     'convert' : int },
                        'skill3'                : {'colName' : u'new_skill3',           'convert' : int },
                        'skillAvailLimit3'      : {'colName' : u'skill_open_step3',     'convert' : int },
                        'skill4'                : {'colName' : u'new_skill4',           'convert' : int },
                        'skillAvailLimit4'      : {'colName' : u'skill_open_step4',     'convert' : int },
                        'skill5'                : {'colName' : u'new_skill5',           'convert' : int },
                        'skillAvailLimit5'      : {'colName' : u'skill_open_step5',     'convert' : int },
                    },
            },
        'C_HERO_LIST' : \
            {
                'fileName'   : u'units',
                'sheetName'  : u'client-hero_list',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'hero_attr'        : {'colName' : u'attr',          'convert' : int },
                        'hero_id1'         : {'colName' : u'hero_id1',      'convert' : int },
                        'hero_id2'         : {'colName' : u'hero_id2',      'convert' : int },
                        'hero_id3'         : {'colName' : u'hero_id3',      'convert' : int },
                    },
            },

        'C_LARGE_UNITS' : \
            {
                'fileName'   : u'large_units',
                'sheetName'  : u'client-large_units',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'cmd1'               : {'colName' : u'cmd1',            'convert'  : covertStr },
                        'cmd2'               : {'colName' : u'cmd2',            'convert'  : covertStr },
                        'flgPrm1'            : {'colName' : u'flgPrm1',         'convert'  : int },
                        'skill1'             : {'colName' : u'skill1',          'convert'  : int },
                        'skill2'             : {'colName' : u'skill2',          'convert'  : int },
                        'prob1'              : {'colName' : u'prob1',           'convert'  : int },
                        'prob2'              : {'colName' : u'prob2',           'convert'  : int },
                        'mvRge1TL'           : {'colName' : u'mvRge1TL',        'convert'  : int },
                        'mvRge1T'            : {'colName' : u'mvRge1T',         'convert'  : int },
                        'mvRge1TR'           : {'colName' : u'mvRge1TR',        'convert'  : int },
                        'mvRge1L'            : {'colName' : u'mvRge1L',         'convert'  : int },
                        'mvRge1R'            : {'colName' : u'mvRge1R',         'convert'  : int },
                        'mvRge1BL'           : {'colName' : u'mvRge1BL',        'convert'  : int },
                        'mvRge1B'            : {'colName' : u'mvRge1B',         'convert'  : int },
                        'mvRge1BR'           : {'colName' : u'mvRge1BR',        'convert'  : int },
                        'mvRge2TL'           : {'colName' : u'mvRge2TL',        'convert'  : int },
                        'mvRge2T'            : {'colName' : u'mvRge2T',         'convert'  : int },
                        'mvRge2TR'           : {'colName' : u'mvRge2TR',        'convert'  : int },
                        'mvRge2L'            : {'colName' : u'mvRge2L',         'convert'  : int },
                        'mvRge2R'            : {'colName' : u'mvRge2R',         'convert'  : int },
                        'mvRge2BL'           : {'colName' : u'mvRge2BL',        'convert'  : int },
                        'mvRge2B'            : {'colName' : u'mvRge2B',         'convert'  : int },
                        'mvRge2BR'           : {'colName' : u'mvRge2BR',        'convert'  : int },
                        'flg'                : {'colName' : u'flg',             'convert'  : int },
                    },
            },

        'C_SCENEINFO' : \
            {
                'fileName'   : u'FB_Config',
                'sheetName'  : u'export-SceneInfo',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'name'               : {'colName' : u'name',            'convert' : covertStr },
                        'modelID'            : {'colName' : u'modelID',         'convert' : covertStr },
                        'map_effect'         : {'colName' : u'map_effect',      'convert' : covertStr },
                        'word'               : {'colName' : u'word',            'convert' : covertStr },
                        'props'              : {'colName' : u'props',           'convert' : int },
                        'bg_id'              : {'colName' : u'bg_id',           'convert' : int },
                        'type'               : {'colName' : u'type',            'convert' : int },
                        'chapter'            : {'colName' : u'chapter',         'convert' : int, 'invalid' : lambda x: x == 0},
                        'prev'               : {'colName' : u'prev',            'convert' : int },
                        'next'               : {'colName' : u'post',            'convert' : int },
                        'jump'               : {'colName' : u'jump',            'convert' : int },
                        'unitsid'            : {'colName' : u'unitsid',         'convert' : int },
                        'mapPath'            : {'colName' : u'firstIcon',       'convert' : covertStr },
                        'islandPath'         : {'colName' : u'islandPath',      'convert' : covertStr },
                        'miniMapPath'        : {'colName' : u'smallIcon',       'convert' : covertStr },
                        'sectionPath'        : {'colName' : u'pchapter',        'convert' : covertStr },
                        'namePath'           : {'colName' : u'pname',           'convert' : covertStr },
                        'subtype'            : {'colName' : u'subtype',         'convert' : int },

                        'fbgroub'            : {'colName' : u'fbgroub',         'convert' : covertStr },
                        'openlv'             : {'colName' : u'openlv',          'convert' : int },
                    },
            },

        'C_SCENE_BG_INFO' : \
            {
                'fileName'   : u'FB_Config',
                'sheetName'  : u'client-sceneBackground',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'mcName'             : {'colName' : u'mcName',          'convert' : covertStr },
                        'far_sprite'         : {'colName' : u'far_sprite',      'convert' : covertStr },
                        'middle_sprite'      : {'colName' : u'middle_sprite',   'convert' : covertStr },
                        'front_sprite'       : {'colName' : u'front_sprite',    'convert' : covertStr },
                        'boss_sprite'        : {'colName' : u'boss_sprite',     'convert' : covertStr },
                        'stone_sprite'       : {'colName' : u'stone_sprite',    'convert' : covertStr },
                        'particle_normal'    : {'colName' : u'particle_normal', 'convert' : covertStr },
                        'particle_boss'      : {'colName' : u'particle_boss',   'convert' : covertStr },
                    },
            },

        'C_FBINFO' : \
            {
                'fileName'   : u'FB_Config',
                'sheetName'  : u'export-FbInfo',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'name'      : {'colName' : u'name',       'convert' : covertStr },
                        'type'      : {'colName' : u'type',       'convert' : int },
                        'sp'        : {'colName' : u'sp',         'convert' : int },
                        'area'      : {'colName' : u'area',       'convert' : int },
                        'sceneID'   : {'colName' : u'sceneID',    'convert' : int },
                        'group1'    : {'colName' : u'group1',     'convert' : int, 'invalid' : lambda x: x == 0, 'ignore' : ['group2', 'group3', 'group4', 'group5']},
                        'group2'    : {'colName' : u'group2',     'convert' : int, 'invalid' : lambda x: x == 0, 'ignore' : ['group3', 'group4', 'group5']},
                        'group3'    : {'colName' : u'group3',     'convert' : int, 'invalid' : lambda x: x == 0, 'ignore' : ['group4', 'group5']},
                        'group4'    : {'colName' : u'group4',     'convert' : int, 'invalid' : lambda x: x == 0, 'ignore' : ['group5']},
                        'group5'    : {'colName' : u'group5',     'convert' : int, 'invalid' : lambda x: x == 0,},
                        'word'      : {'colName' : u'word',       'convert' : covertStr , },
                        'stone_num' : {'colName' : u'stone_num',  'convert' : int, },
                        'desc'      : {'colName' : u'fbdepict',   'convert' : covertStr , },
                        'index'     : {'colName' : u'fborder',    'convert' : int, },
                        'rewards'   : {'colName' : u'makingdrop', 'convert' : covertStr , 'check'  : checkJsonStr,},
                        'buffid'    : {'colName' : u'buffid',     'convert' : int, },
                        'boss_type' : {'colName' : u'boss_type',  'convert' : int, },
                        'boss_icon' : {'colName' : u'boss_icon',  'convert' : int, },
                    },
            },

        'C_MONSTERGROUP' : \
            {
                'fileName'   : u'FB_Config',
                'sheetName'  : u'export-monstergroup',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'monster_id1'    :{'colName':u'monster_id1',    'convert':int, 'invalid' : lambda x:x==0, 'ignore' : ['monster_level1','monster_star1','post1'] },
                        'monster_level1' :{'colName':u'monster_level1', 'convert':int, },
                        'monster_star1'  :{'colName':u'monster_star1',  'convert':int, },
                        'post1'          :{'colName':u'post1',          'convert':int, 'invalid' : lambda x:x==0 },
                        'skill_level1'   :{'colName':u'skill_level1',   'convert':str, },
                        'monster_id2'    :{'colName':u'monster_id2',    'convert':int, 'invalid' : lambda x:x==0, 'ignore' : ['monster_level2','monster_star2','post2'] },
                        'monster_level2' :{'colName':u'monster_level2', 'convert':int, },
                        'monster_star2'  :{'colName':u'monster_star2',  'convert':int, },
                        'post2'          :{'colName':u'post2',          'convert':int, 'invalid' : lambda x:x==0 },
                        'skill_level2'   :{'colName':u'skill_level2',   'convert':str, },
                        'monster_id3'    :{'colName':u'monster_id3',    'convert':int, 'invalid' : lambda x:x==0, 'ignore' : ['monster_level3','monster_star3','post3'] },
                        'monster_level3' :{'colName':u'monster_level3', 'convert':int, },
                        'monster_star3'  :{'colName':u'monster_star3',  'convert':int, },
                        'post3'          :{'colName':u'post3',          'convert':int, 'invalid' : lambda x:x==0 },
                        'skill_level3'   :{'colName':u'skill_level3',   'convert':str, },
                        'monster_id4'    :{'colName':u'monster_id4',    'convert':int, 'invalid' : lambda x:x==0, 'ignore' : ['monster_level4','monster_star4','post4'] },
                        'monster_level4' :{'colName':u'monster_level4', 'convert':int, },
                        'monster_star4'  :{'colName':u'monster_star4',  'convert':int, },
                        'post4'          :{'colName':u'post4',          'convert':int, 'invalid' : lambda x:x==0 },
                        'skill_level4'   :{'colName':u'skill_level4',   'convert':str, },
                    },
            },

        'C_BUFF' : \
            {
                'fileName'   : u'FB_Config',
                'sheetName'  : u'client-buff',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'last_round'        : {'colName' : u'term',             'convert' : int },
                        'kind'              : {'colName' : u'type',             'convert' : int },
                        'val'               : {'colName' : u'val',              'convert' : int },
                        'type'              : {'colName' : u'aim',              'convert' : covertStr },
                    },
            },

        'C_BUFF_GROUP' : \
            {
                'fileName'   : u'FB_Config',
                'sheetName'  : u'client-buff_bag',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'buffid'            : {'colName' : u'buffid',           'convert' : covertStr },
                    },
            },

        'C_SKILLUP' : \
            {
                'fileName'    : u'skillup',
                'sheetName'   : u'export-skillup',
                'primeKey'    : u'id',
                'increment'  : True,
                'readOnlyCol' : \
                    {
                        'pose1'             : {'colName' : u'pose1',            'convert' : int },
                        'pose2'             : {'colName' : u'pose2',            'convert' : int },
                        'pose3'             : {'colName' : u'pose3',            'convert' : int },
                        'pose4'             : {'colName' : u'pose4',            'convert' : int },
                        'pose5'             : {'colName' : u'pose5',            'convert' : int },
                    },
            },

       'C_LVUP' : \
            {
               'fileName'   : u'Actor_Config',
               'sheetName'  : u'export-Lvup',
               'primeKey'   : u'lv',
               'increment'  : True,
               'readOnlyCol': \
                    {
                        'lv'                 : {'colName' : u'lv',               'convert' : int,},
                        'exp'                : {'colName' : u'exp',              'convert' : int,},
                        'power'              : {'colName' : u'power',            'convert' : int,},
                        'sp'                 : {'colName' : u'sp',               'convert' : int,},
                        'maxexp'             : {'colName' : u'maxexp',           'convert' : int,},
                        'maxpower'           : {'colName' : u'maxpower',         'convert' : int,},
                        'maxsp'              : {'colName' : u'maxsp',            'convert' : int,},
                        # 模块等级限制 不直接读取，仅保存为开启的数据，开启条件由公式计算
                        # 公会限制
                        'FACTION'            : {'colName' : u'union',            'convert' : int,       'invalid' : lambda x: x > 0,},
                        # PVP限制
                        'PVP'                : {'colName' : u'pvp',              'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 精英本限制
                        'ELITE_CHAPTER'      : {'colName' : u'hard_fb',          'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 装备限制
                        'EQUIP'              : {'colName' : u'equip',            'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 英雄升级限制
                        'HERO_LEVELUP'       : {'colName' : u'levelup',          'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 英雄进化限制
                        'HERO_EVO'           : {'colName' : u'evo',              'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 英雄突破限制
                        'HERO_BREAKTHROUGH'  : {'colName' : u'star',             'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 争夺战1限制
                        'FARM1'              : {'colName' : u'get_money1',       'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 争夺战2限制
                        'FARM2'              : {'colName' : u'get_exp1',         'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 大闹天宫
                        'UPROAR'             : {'colName' : u'ticket',           'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 大闹天宫冲刺
                        'UPROAR_EX'          : {'colName' : u'ticket_ex',        'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 普通炼化
                        'SMELT'              : {'colName'  : u'refine',          'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 装备炼化
                        'SMELT_EQUIP'        : {'colName'  : u'refine_equip',    'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 法宝炼化
                        'SMELT_TALISMAN'     : {'colName'  : u'refine_fabao',    'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 醉仙斗
                        'FARFIGHT'           : {'colName'  : u'rob',             'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 聊天
                        'CHATROOM'           : {'colName'  : u'chatroom',        'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 任务
                        'MISSION'            : {'colName'  : u'mission',         'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 炼化
                        'GOLDTOMONEY'        : {'colName' : u'golden_finger',    'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 天庭商店
                        'SKYSTORE'           : {'colName' : u'heavenstore',      'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 金角商店
                        'GOLDSTORE'          : {'colName' : u'goldenstore',      'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 银角商店
                        'SLIVERSTORE'        : {'colName' : u'sliverstore',      'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 点将台
                        'HOTUNITS'           : {'colName' : u'hotunits',         'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 扫荡
                        'CLEANUP'            : {'colName' : u'cleanUp',          'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 召唤
                        'SUMMON'            : {'colName' : u'lottery',           'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 探险
                        'EXPLORE'            : {'colName' : u'explore',          'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 拜八仙
                        'EIGHT_IMMORTALS'    : {'colName' : u'visit',            'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 化缘
                        'BEG_ALMS'           : {'colName' : u'eat',              'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 直接下一关
                        'QUICK_START_SECTION': {'colName' : u'keepfb',           'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 神将渡魂
                        'HERO_COMBINATION'   : {'colName' : u'units_compose',    'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 装备重铸
                        'EQUIP_COMBINATION'  : {'colName' : u'equip_compose',    'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 当日冒险礼包单选
                        'DAILY_SINGLE_GIFTBAG': {'colName' : u'one_gift',         'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 当日多选礼包
                        'DAILY_MULTI_GIFTBAG' : {'colName' : u'several_gift',     'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 洞天福地
                        'DONG_TIAN_FU_DI'     : {'colName' : u'blessedSpot',      'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 晶石召唤
                        'CALL_SPAR_HERO'      : {'colName' : u'spar',             'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 好友
                        'FRIENDS'             : {'colName' : u'friends',          'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 秘境
                        'MYSTICAL_LANDS'      : {'colName' : u'relicfb',          'convert' : int,       'invalid' : lambda x: x > 0,},
                        'TAP'                 : {'colName' : u'atk_monster',      'convert' : int,       'invalid' : lambda x: x > 0,},
                        'GREEDY'              : {'colName' : u'golden_sliver_hill','convert' : int,       'invalid' : lambda x: x > 0,},
                        'KNOWLEDGE'           : {'colName' : u'knowledge',         'convert' : int,       'invalid' : lambda x: x > 0,},
                        'RANK'                : {'colName' : u'rank',              'convert' : int,       'invalid' : lambda x: x > 0,},
                        'ENCHANT'             : {'colName' : u'enchant',           'convert' : int,       'invalid' : lambda x: x > 0,},
                        'DLCFB'               : {'colName' : u'dlcfb',             'convert' : int,       'invalid' : lambda x: x > 0,},
                        'LIMIT_TIME_GIFT'     : {'colName' : u'limit_time_gift',   'convert' : int,       'invalid' : lambda x: x > 0,},
                        # 同门
                        'FELLOW'              : {'colName' : u'family',            'convert' : int,       'invalid' : lambda x: x > 0,},
                        'ACTIVE_CHAPTER'      : {'colName' : u'active_chapter',    'convert' : int,       'invalid' : lambda x: x > 0,},
                        'RANDOM_COPMOSE'      : {'colName' : u'random_compose',    'convert' : int,       'invalid' : lambda x: x > 0,},
                        'DECOMPOSE'           : {'colName' : u'decompose',         'convert' : int,       'invalid' : lambda x: x > 0,},
                        'MAZE'                : {'colName' : u'maze',              'convert' : int,       'invalid' : lambda x: x > 0,},
                        'SKILL_LV_UP'         : {'colName' : u'skill_up',          'convert' : int,       'invalid' : lambda x: x > 0,},
                        'DAILY_PVP'           : {'colName' : u'daily_pvp',         'convert' : int,       'invalid' : lambda x: x > 0,},
                        'AMBITION'            : {'colName' : u'ambition',          'convert' : int,       'invalid' : lambda x: x > 0,},
                        'STRENGTHEN'          : {'colName' : u'strengthen',        'convert' : int,       'invalid' : lambda x: x > 0,},
                        'GOLDTOSOUL'          : {'colName' : u'golden_soul',       'convert' : int,       'invalid' : lambda x: x > 0,},
                        'GOLDEN_CITY'         : {'colName' : u'golden_city',       'convert' : int,       'invalid' : lambda x: x > 0,},
                        'PLAYER_EQUIPMENT'    : {'colName' : u'player_equipment',  'convert' : int,       'invalid' : lambda x: x > 0,},
                        'PVP_TOWER'    		  : {'colName' : u'pvp_tower',         'convert' : int,       'invalid' : lambda x: x > 0,},
                    },

                #'functionCol': \
                #    {
                #        'FACTION'            : '''function(config, key) return config._FACTION or 1 end''',
                #        'PVP'                : '''function(config, key) return config._PVP or 1 end''',
                #        'ELITE_CHAPTER'      : '''function(config, key) return config._ELITE_CHAPTER or 1 end''',
                #        'EQUIP'              : '''function(config, key) return config._EQUIP or 1 end''',
                #        'HERO_LEVELUP'       : '''function(config, key) return config._HERO_LEVELUP or 1 end''',
                #        'HERO_EVO'           : '''function(config, key) return config._HERO_EVO or 1 end''',
                #        'HERO_BREAKTHROUGH'  : '''function(config, key) return config._HERO_BREAKTHROUGH or 1 end''',
                #        'FARM1'              : '''function(config, key) return config._FARM1 or ((key > 1) and (C_LVUP[key - 1].FARM1 + 1) or 1) end''',
                #        'FARM2'              : '''function(config, key) return config._FARM2 or ((key > 1) and (C_LVUP[key - 1].FARM2 + 1) or 1) end''',
                #        'UPROAR'             : '''function(config, key) return config._UPROAR         or 1 end''',
                #        'ARTIFICE'           : '''function(config, key) return config._ARTIFICE       or 1 end''',
                #        'ARTIFICE_MAGIC'     : '''function(config, key) return config._ARTIFICE_MAGIC or 1 end''',
                #        'FARFIGHT'           : '''function(config, key) return config._FARFIGHT       or 1 end''',
                #        'CHATROOM'           : '''function(config, key) return config._CHATROOM       or 1 end''',
                #        'MISSION'            : '''function(config, key) return config._MISSION        or 1 end''',
                #        'GOLDTOMONEY'        : '''function(config, key) return config._GOLDTOMONEY    or 1 end''',
                #        'SKYSTORE'           : '''function(config, key) return config._GOLDSTORE      or 1 end''',
                #        'GOLDSTORE'          : '''function(config, key) return config._GOLDSTORE      or 1 end''',
                #        'SLIVERSTORE'        : '''function(config, key) return config._SLIVERSTORE    or 1 end''',
                #        'HOTUNITS'           : '''function(config, key) return config._HOTUNITS       or 1 end''',
                #        'CLEANUP'            : '''function(config, key) return config._CLEANUP        or 1 end''',
                #    },
            },

        'C_LVUP_SHOW'  : \
            {
                'fileName'   : u'Actor_Config',
                'sheetName'  : u'client-lvup_icon',
                'primeKey'   : u'level ',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'icon'     : {'colName' : u'icon',         'convert' : covertStr },
                    },
            },

        #'C_ACHIEVEMENT' : \
        #    {
        #        'fileName'   : u'Rewards_Config',
        #        'sheetName'  : u'export-Achievement',
        #        'primeKey'   : u'id',
        #        'increment'  : True,
        #        'readOnlyCol': \
        #            {
        #                'id'                 : {'colName' : u'id',              'convert' : int },
        #                'name'               : {'colName' : u'name',            'convert' : covertStr },
        #                'number'             : {'colName' : u'number',          'convert' : int },
        #                'type'               : {'colName' : u'type',            'convert' : int },
        #                'itemID'             : {'colName' : u'itemID',          'convert' : int },
        #                'amount'             : {'colName' : u'amount',          'convert' : int },
        #            },
        #    },

        'C_HEROGROWTH'  : \
            {
                'fileName'   : u'HeroGrowth',
                'sheetName'  : u'export-herogrowth',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'evo_levellimit'     : {'colName' : u'hero_lv',         'convert' : int },
                        'evo_cost'           : {'colName' : u'evo_cost',        'convert' : int },
                        'breed_cost'         : {'colName' : u'breed_cost',      'convert' : int },
                    },
            },


        'C_BREAKTHROUGH'  : \
            {
                'fileName'   : u'units',
                'sheetName'  : u'export-break',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'hpRatio'            : {'colName' : u'bHP',             'convert' : float },
                        'atkRatio'           : {'colName' : u'batk',            'convert' : float },
                        'defRatio'           : {'colName' : u'bdef',            'convert' : float },
                        'critRatio'          : {'colName' : u'bcrit',           'convert' : float },
                        'dodgeRatio'         : {'colName' : u'bdodge',          'convert' : float },
                        'amountRatio'        : {'colName' : u'amount',          'convert' : int },

                        'stifle'             : {'colName' : u'stifle',          'convert' : float },
                        'restraint'          : {'colName' : u'restraint',       'convert' : float },

                        'price'              : {'colName' : u'silver',          'convert' : int },
                        'max_level'          : {'colName' : u'lv_limit',        'convert' : int },
                        'break_index'        : {'colName' : u'data_id',         'convert' : int },
                    },
            },

        'C_CAREERTALK' : \
            {
                'fileName'   : u'FBtalk',
                'sheetName'  : u'client-careertalk',
                'primeKey'   : u'id',
                'readOnlyCol': \
                    {
                        'fbid'               : {'colName' : u'fbid',            'convert' : int},
                        'monsterid1'         : {'colName' : u'monsterid1',      'convert' : int,    'invalid' : lambda x: x == -1,    'ignore' : ['window1', 'monstername1', 'content1']},
                        'window1'            : {'colName' : u'window1',         'convert' : int},
                        'monstername1'       : {'colName' : u'monstername1',    'convert' : covertStr},
                        'content1'           : {'colName' : u'content1',        'convert' : covertStr},
                        'monsterid2'         : {'colName' : u'monsterid2',      'convert' : int,    'invalid' : lambda x: x == -1,    'ignore' : ['window2', 'monstername2', 'content2']},
                        'window2'            : {'colName' : u'window2',         'convert' : int},
                        'monstername2'       : {'colName' : u'monstername2',    'convert' : covertStr},
                        'content2'           : {'colName' : u'content2',        'convert' : covertStr},
                        'monsterid3'         : {'colName' : u'monsterid3',      'convert' : int,    'invalid' : lambda x: x == -1,    'ignore' : ['window3', 'monstername3', 'content3']},
                        'window3'            : {'colName' : u'window3',         'convert' : int},
                        'monstername3'       : {'colName' : u'monstername3',    'convert' : covertStr},
                        'content3'           : {'colName' : u'content3',        'convert' : covertStr},
                        'monsterid4'         : {'colName' : u'monsterid4',      'convert' : int,    'invalid' : lambda x: x == -1,    'ignore' : ['window4', 'monstername4', 'content4']},
                        'window4'            : {'colName' : u'window4',         'convert' : int},
                        'monstername4'       : {'colName' : u'monstername4',    'convert' : covertStr},
                        'content4'           : {'colName' : u'content4',        'convert' : covertStr},
                    },
            },

        'C_MODULETALK' : \
            {
                'fileName'   : u'FBtalk',
                'sheetName'  : u'client-moduletalk',
                'primeKey'   : u'id',
                'readOnlyCol': \
                    {
                        'modulename'         : {'colName' : u'modulename',      'convert' : covertStr},
                        'monsterid1'         : {'colName' : u'monsterid1',      'convert' : int,    'invalid' : lambda x: x == -1,    'ignore' : ['window1', 'monstername1', 'content1']},
                        'window1'            : {'colName' : u'window1',         'convert' : int},
                        'monstername1'       : {'colName' : u'monstername1',    'convert' : covertStr},
                        'content1'           : {'colName' : u'content1',        'convert' : covertStr},
                        'monsterid2'         : {'colName' : u'monsterid2',      'convert' : int,    'invalid' : lambda x: x == -1,    'ignore' : ['window2', 'monstername2', 'content2']},
                        'window2'            : {'colName' : u'window2',         'convert' : int},
                        'monstername2'       : {'colName' : u'monstername2',    'convert' : covertStr},
                        'content2'           : {'colName' : u'content2',        'convert' : covertStr},
                        'monsterid3'         : {'colName' : u'monsterid3',      'convert' : int,    'invalid' : lambda x: x == -1,    'ignore' : ['window3', 'monstername3', 'content3']},
                        'window3'            : {'colName' : u'window3',         'convert' : int},
                        'monstername3'       : {'colName' : u'monstername3',    'convert' : covertStr},
                        'content3'           : {'colName' : u'content3',        'convert' : covertStr},
                        'monsterid4'         : {'colName' : u'monsterid4',      'convert' : int,    'invalid' : lambda x: x == -1,    'ignore' : ['window4', 'monstername4', 'content4']},
                        'window4'            : {'colName' : u'window4',         'convert' : int},
                        'monstername4'       : {'colName' : u'monstername4',    'convert' : covertStr},
                        'content4'           : {'colName' : u'content4',        'convert' : covertStr},
                    },
            },

        'C_STRENGTHEN' : \
            {
                'fileName'   : u'unions',
                'sheetName'  : u'export-strengthen',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'lv'                : {'colName' : u'lv',              'convert' : int },
                        'cost'              : {'colName' : u'cost',            'convert' : int },
                        'study'             : {'colName' : u'study',           'convert' : int },
                        'uhp'               : {'colName' : u'uhp',             'convert' : int },
                        'uatk'              : {'colName' : u'uatk',            'convert' : int },
                        'ubj'               : {'colName' : u'ubj',             'convert' : float },
                        'udef'              : {'colName' : u'udef',            'convert' : float },
                    },
            },

        'C_UNIONS' : \
            {
                'fileName'   : u'unions',
                'sheetName'  : u'export-unions',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'lv'                : {'colName' : u'lv',             'convert' : int },
                        'num'               : {'colName' : u'num',            'convert' : int },
                        'exp'               : {'colName' : u'exp',            'convert' : int },
                    },
            },

        'C_HOTUNITDESC' : \
            {
                'fileName'   : u'hotunit',
                'sheetName'  : u'client-desc',
                'primeKey'   : u'id',
                'readOnlyCol': \
                    {
                        'desc'              : {'colName' : u'desc',           'convert' : covertStr},
                    },
            },

        'C_VIP' : \
            {
                'fileName'   : u'viplist',
                'sheetName'  : u'export-Vip',
                'primeKey'   : u'level',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'amount'           : {'colName' : u'amount',         'convert' : int},
                    },
            },

        'C_CONVERT' : \
            {
                'fileName'   : u'piecesystem',
                'sheetName'  : u'export-convert',
                'primeKey'   : u'id',
                'readOnlyCol': \
                    {
                        'num'              : {'colName' : u'num',            'convert' : int},
                    },
            },

        'C_GRAD' : \
            {
                'fileName'   : u'pvp',
                'sheetName'  : u'export-pvp_grad',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'score'            : {'colName' : u'score',          'convert' : int },
                        'battle_num'       : {'colName' : u'battle_num',     'convert' : int },
                        'rank'             : {'colName' : u'ranking',        'convert' : int },
                        'grad_png'         : {'colName' : u'grad_png',       'convert' : int },
                    },
            },

        'C_ITEMS' : \
            {
                'fileName'   : u'items',
                'sheetName'  : u'export-items',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'type'            : {'colName' : u'type',          'convert' : int },
                        'refConfigID'     : {'colName' : u'index',         'convert' : int },
                        'destConfigID'    : {'colName' : u'piece_index',   'convert' : int,   'invalid' : lambda x : x <= 0},
                        'iconid'          : {'colName' : u'iconid',        'convert' : int },
                        'mask'            : {'colName' : u'maskIcon',      'convert' : int },
                        'rarity'          : {'colName' : u'rarity',        'convert' : int },
                        'name'            : {'colName' : u'name',          'convert' : covertStr ,   'invalid' : lambda x : x == "" },
                        'desc'            : {'colName' : u'desc',          'convert' : covertStr ,   'invalid' : lambda x : x == "" },
                    },
            },
        'C_SKILL_CONFIG'  : \
            {
                'fileName'   : u'skill_new',
                'sheetName'  : u'client-new_skill',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'name'                  : {'colName' : u'name',                 'convert' : covertStr },
                        'desc'                  : {'colName' : u'desc',                 'convert' : covertStr },
                        'effects'               : {'colName' : u'effects',              'convert' : covertStr },
                        'probability'           : {'colName' : u'probability',          'convert' : int },
                        'is_aura'               : {'colName' : u'is_aura',              'convert' : int },
                        'is_additional'         : {'colName' : u'is_additional',        'convert' : int },
                        'in_cd'                 : {'colName' : u'in_cd',                'convert' : int },
                        'round'                 : {'colName' : u'round',                'convert' : int },
                        'action'                : {'colName' : u'action',               'convert' : int },
                        'active'                : {'colName' : u'active',               'convert' : int },
                        'rge'                   : {'colName' : u'rge',                  'convert' : int },
                        'attr'                  : {'colName' : u'attr',                 'convert' : int },
                        'state'                 : {'colName' : u'state',                'convert' : int },
                        'attr_type'             : {'colName' : u'attr_type',            'convert' : int },
                        'relative'              : {'colName' : u'relative',             'convert' : int },
                        'param'                 : {'colName' : u'param',                'convert' : int },
                        'compare_type'          : {'colName' : u'compare_type',         'convert' : int },
                        'src_relationship'      : {'colName' : u'src_relationship',     'convert' : int },
                        'src_attr'              : {'colName' : u'src_attr',             'convert' : int },
                        'src_state'             : {'colName' : u'src_state',            'convert' : int },
                        'src_attr_type'         : {'colName' : u'src_attr_type',        'convert' : int },
                        'src_relative'          : {'colName' : u'src_relative',         'convert' : int },
                        'src_param'             : {'colName' : u'src_param',            'convert' : int },
                        'src_compare_type'      : {'colName' : u'src_compare_type',     'convert' : int },
                        'target_relationship'   : {'colName' : u'target_relationship',  'convert' : int },
                        'target_attr'           : {'colName' : u'target_attr',          'convert' : int },
                        'target_state'          : {'colName' : u'target_state',         'convert' : int },
                        'target_attr_type'      : {'colName' : u'target_attr_type',     'convert' : int },
                        'target_relative'       : {'colName' : u'target_relative',      'convert' : int },
                        'target_param'          : {'colName' : u'target_param',         'convert' : int },
                        'target_compare_type'   : {'colName' : u'target_compare_type',  'convert' : int },
                        'icon'                  : {'colName' : u'skill_png',            'convert' : int },
                        'special_effect_name'   : {'colName' : u'special_effect_name',  'convert' : covertStr },
                        'special_effect_name_2' : {'colName' : u'special_effect_name_2','convert' : covertStr },
                        'play_effect_delay'     : {'colName' : u'play_effect_delay',    'convert' : float },
                        'play_effect_type'      : {'colName' : u'play_effect_type',     'convert' : int },
                    },
            },
        'C_SKILL_EFFECT_CONFIG'  : \
            {
                'fileName'   : u'skill_new',
                'sheetName'  : u'client-skillbuff',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'id'                    : {'colName' : u'id',                       'convert' : int },
                        'name'                  : {'colName' : u'name',                     'convert' : covertStr },
                        'target_type'           : {'colName' : u'type',                     'convert' : int },
                        'targets'               : {'colName' : u'targets',                  'convert' : covertStr },
                        'rge'                   : {'colName' : u'rge',                      'convert' : int },
                        'attr'                  : {'colName' : u'attr',                     'convert' : int },
                        'state_param'           : {'colName' : u'state_param',              'convert' : covertStr },
                        'kind'                  : {'colName' : u'kind',                     'convert' : int },
                        'relative'              : {'colName' : u'relative',                 'convert' : int },
                        'param'                 : {'colName' : u'param',                    'convert' : int },
                        'lv_param'              : {'colName' : u'param_lv_grow',            'convert' : int },
                        'abs_param'             : {'colName' : u'abs_param',                'convert' : int },
                        'lv_abs_param'          : {'colName' : u'ads_param_lv_grow',        'convert' : int },
                        'lv_probability'        : {'colName' : u'probability_lv_grow',      'convert' : int },
                        'tri_param'             : {'colName' : u'c_param',                  'convert' : covertStr },
                        'round'                 : {'colName' : u'round',                    'convert' : int },
                        'additional'            : {'colName' : u'additional',               'convert' : int },
                        'additional_beak_back'  : {'colName' : u'additional_beak_back',     'convert' : int },
                        'display_type'          : {'colName' : u'display_type',             'convert' : int },
                    },
            },

        'C_SUMMONS_SHOW_LIST'  : \
            {
                'fileName'   : u'Mall',
                'sheetName'  : u'client-extract',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'type'            : {'colName' : u'type',           'convert' : int },
                        'u_id'            : {'colName' : u'u_id',           'convert' : int },
                        'name'            : {'colName' : u'name',           'convert' : covertStr },
                    },
            },

        'C_FARM'   : \
            {
                'fileName'   : u'resource',
                'sheetName'  : u'export-resource',
                'primeKey'   : u'house_lv',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'farm1_size'    : {'colName' : u'house1_size',    'convert' : int },
                        'farm1_speed'   : {'colName' : u'house1_speed',   'convert' : int },
                        'farm1_line'    : {'colName' : u'house1_line',    'convert' : int },
                        'farm2_size'    : {'colName' : u'house2_size',    'convert' : int },
                        'farm2_speed'   : {'colName' : u'house2_speed',   'convert' : int },
                        'farm2_line'    : {'colName' : u'house2_line',    'convert' : int },
                    },
            },

        'C_FARMER'   : \
            {
                'fileName'   : u'resource',
                'sheetName'  : u'export-herospeed',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'type'          : {'colName' : u'type',            'convert' : int },
                        'rarity'        : {'colName' : u'rarity',          'convert' : int },
                        'speed1'        : {'colName' : u'speed1',          'convert' : int },
                        'speed2'        : {'colName' : u'speed2',          'convert' : int },
                    },
            },

        #'C_EQUIPS'   : \
        #    {
        #        'fileName'   : u'equipment',
        #        'sheetName'  : u'export-equip',
        #        'primeKey'   : u'eid',
        #        'increment'  : True,
        #        'readOnlyCol': \
        #            {
        #                'ename'        : {'colName' : u'ename' ,          'convert' : covertStr },
        #                'ekind'        : {'colName' : u'ekind' ,          'convert' : int },
        #                'ecolor'       : {'colName' : u'ecolor',          'convert' : int },
        #                'ATK'          : {'colName' : u'ATK'   ,          'convert' : int },
        #                'AGU'          : {'colName' : u'AGU'   ,          'convert' : float },
        #                'AGV'          : {'colName' : u'AGV'   ,          'convert' : float },
        #                'HP'           : {'colName' : u'HP'    ,          'convert' : int },
        #                'HGU'          : {'colName' : u'HGU'   ,          'convert' : float },
        #                'HGV'          : {'colName' : u'HGV'   ,          'convert' : float },
        #                'DEF'          : {'colName' : u'DEF'   ,          'convert' : int },
        #                'DGU'          : {'colName' : u'DGU'   ,          'convert' : float },
        #                'DGV'          : {'colName' : u'DGV'   ,          'convert' : float },
        #                'EVA'          : {'colName' : u'EVA'   ,          'convert' : float },
        #                'EGU'          : {'colName' : u'EGU'   ,          'convert' : float },
        #                'EGV'          : {'colName' : u'EGV'   ,          'convert' : float },
        #                'CRI'          : {'colName' : u'CRI'   ,          'convert' : float },
        #                'CGU'          : {'colName' : u'CGU'   ,          'convert' : float },
        #                'CGV'          : {'colName' : u'CGV'   ,          'convert' : float },
        #                'eq'           : {'colName' : u'eq'    ,          'convert' : int },
        #                'iconid'       : {'colName' : u'iconid',          'convert' : int },
        #                'picid'        : {'colName' : u'picid',           'convert' : int },
        #                'pnum'         : {'colName' : u'pnum',            'convert' : int },
        #                'issuit'       : {'colName' : u'issuit',          'convert' : int },
        #                'isexclusive'  : {'colName' : u'isexclusive',     'convert' : int },
        #                'desc'         : {'colName' : u'desc'  ,          'convert' : covertStr },
        #            },
        #    },

        'C_EQUIP_ADVANCE_LIMIT'   : \
            {
                'fileName'   : u'equipment',
                'sheetName'  : u'export-equipadvancelimit',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'ecolor'       : {'colName' : u'ecolor',          'convert' : int },
                        'ekind'        : {'colName' : u'ekind' ,          'convert' : int },
                        'stlimit'      : {'colName' : u'stlimit',         'convert' : int },
                        'pcount'       : {'colName' : u'pcount',          'convert' : int },
                    },
            },

        'C_EQUIP_EXCLUSIVE'   : \
            {
                'fileName'   : u'equipment',
                'sheetName'  : u'export-exclusive',
                'primeKey'   : u'exclid',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'unit1'       : {'colName' : u'unit1',          'convert' : int },
                        'unit2'       : {'colName' : u'unit2',          'convert' : int },
                        'unit3'       : {'colName' : u'unit3',          'convert' : int },
                        'unit4'       : {'colName' : u'unit4',          'convert' : int },
                        'ATK'         : {'colName' : u'ATK'  ,          'convert' : int },
                        'HP'          : {'colName' : u'HP'   ,          'convert' : int },
                        'DEF'         : {'colName' : u'DEF'  ,          'convert' : int },
                        'EVA'         : {'colName' : u'EVA'  ,          'convert' : int },
                        'CRI'         : {'colName' : u'CRI'  ,          'convert' : int },
                    },
            },

        'C_EQUIP_SUIT'   : \
            {
                'fileName'   : u'equipment',
                'sheetName'  : u'export-suit',
                'primeKey'   : u'suitid',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'equip1'       : {'colName' : u'equip1',          'convert' : int },
                        'equip2'       : {'colName' : u'equip2',          'convert' : int },
                        'equip3'       : {'colName' : u'equip3',          'convert' : int },
                        'equip4'       : {'colName' : u'equip4',          'convert' : int },
                        'equip5'       : {'colName' : u'equip5',          'convert' : int },
                        'equip6'       : {'colName' : u'equip6',          'convert' : int },
                        'HP2'          : {'colName' : u'HP2',             'convert' : int },
                        'ATK2'         : {'colName' : u'ATK2',            'convert' : int },
                        'DEF2'         : {'colName' : u'DEF2',            'convert' : int },
                        'EVA2'         : {'colName' : u'EVA2',            'convert' : int },
                        'CRI2'         : {'colName' : u'CRI2',            'convert' : int },
                        'HP3'          : {'colName' : u'HP3',             'convert' : int },
                        'ATK3'         : {'colName' : u'ATK3',            'convert' : int },
                        'DEF3'         : {'colName' : u'DEF3',            'convert' : int },
                        'EVA3'         : {'colName' : u'EVA3',            'convert' : int },
                        'CRI3'         : {'colName' : u'CRI3',            'convert' : int },
                        'HP4'          : {'colName' : u'HP4',             'convert' : int },
                        'ATK4'         : {'colName' : u'ATK4',            'convert' : int },
                        'DEF4'         : {'colName' : u'DEF4',            'convert' : int },
                        'EVA4'         : {'colName' : u'EVA4',            'convert' : int },
                        'CRI4'         : {'colName' : u'CRI4',            'convert' : int },
                        'HP5'          : {'colName' : u'HP5',             'convert' : int },
                        'ATK5'         : {'colName' : u'ATK5',            'convert' : int },
                        'DEF5'         : {'colName' : u'DEF5',            'convert' : int },
                        'EVA5'         : {'colName' : u'EVA5',            'convert' : int },
                        'CRI5'         : {'colName' : u'CRI5',            'convert' : int },
                        'HP6'          : {'colName' : u'HP6',             'convert' : int },
                        'ATK6'         : {'colName' : u'ATK6',            'convert' : int },
                        'DEF6'         : {'colName' : u'DEF6',            'convert' : int },
                        'EVA6'         : {'colName' : u'EVA6',            'convert' : int },
                        'CRI6'         : {'colName' : u'CRI6',            'convert' : int },
                    },
            },

        'C_DROPLOCATION' : \
            {
                'fileName'   : u'droplocation',
                'sheetName'  : u'client-droplocation',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'iconId'             : {'colName' : u'icon'         ,   'convert' : covertStr},
                        'DropIDs'            : {'colName' : u'Drop_location',   'convert' : covertStr},
                        'StoreIDs'           : {'colName' : u'StoreID'      ,   'convert' : covertStr},
                        'isDrop'             : {'colName' : u'isDrop'       ,   'convert' : int},
                        'isStore'            : {'colName' : u'isStore'      ,   'convert' : int},

                        'SummonIDs'          : {'colName' : u'summonID'     ,   'convert' : covertStr},
                        'isSummon'           : {'colName' : u'isSummon'     ,   'convert' : int},
                        'composeID'          : {'colName' : u'composeID'    ,   'convert' : int},
                        'isCompose'          : {'colName' : u'isCompose'    ,   'convert' : int},
                        'isTransform'        : {'colName' : u'isChange'     ,   'convert' : int},
                    },
            },

        'C_HERO_COMBINE' : \
            {
                'fileName'   : u'compose',
                'sheetName'  : u'export-units_compose',
                'primeKey'   : u'id',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'order'             : {'colName' : u'seq'           ,   'convert' : int},
                        'openLv'            : {'colName' : u'openlv'        ,   'convert' : int},
                        'unlockLv'          : {'colName' : u'unlocklv'      ,   'convert' : int},
                        'matrls'            : {'colName' : u'units1'        ,   'convert' : covertStr},
                        'moneyCost'         : {'colName' : u'coin'          ,   'convert' : int,   'invalid' : lambda x : x <= 0},
                        'soulCost'          : {'colName' : u'soul'          ,   'convert' : int,   'invalid' : lambda x : x <= 0},
                    },
            },

        'C_EVO_MATRL_COMBINE' : \
            {
                'fileName'   : u'compose',
                'sheetName'  : u'export-stuff_compose',
                'primeKey'   : u'id',
                'readOnlyCol': \
                    {
                        'prev'            : {'colName' : u'pre-stuffid'     ,   'convert' : int},
                        'next'            : {'colName' : u'stuffid'         ,   'convert' : int},
                        'count'           : {'colName' : u'count'           ,   'convert' : int},
                        'moneyCost'       : {'colName' : u'coin'            ,   'convert' : int,   'invalid' : lambda x : x <= 0},
                        'soulCost'        : {'colName' : u'soul'            ,   'convert' : int,   'invalid' : lambda x : x <= 0},
                        'order'           : {'colName' : u'order'           ,   'convert' : int},
                    },
            },

        'C_EQUIP_COMPOSE' : \
            {
                'fileName'    : u'compose',
                'sheetName'   : u'export-equip_compose',
                'primeKey'    : u'id',
                'increment'  : True,
                'readOnlyCol' : \
                    {
                        'openLv'          : {'colName' : u'openlv'          ,   'convert' : int},
                        'unlockLv'        : {'colName' : u'unlocklv'        ,   'convert' : int},
                        'equips'          : {'colName' : u'equip1'          ,   'convert' : covertStr},
                        'moneyCost'       : {'colName' : u'coin'            ,   'convert' : int, 'invalid' : lambda x :x <= 0},
                        'soulCost'        : {'colName' : u'soul'            ,   'convert' : int, 'invalid' : lambda x :x <= 0},
                    },
            },
        'C_PVP_BUFF' : \
            {
                'fileName'    : u'pvp',
                'sheetName'   : u'export-wining_buff',
                'primeKey'    : u'id',
                'readOnlyCol' : \
                    {
                        'buff1'       : {'colName' : u'buff1'       ,   'convert' : int},
                        'parm1'       : {'colName' : u'param1'      ,   'convert' : int},
                        'buff2'       : {'colName' : u'buff2'       ,   'convert' : int},
                        'parm2'       : {'colName' : u'param2'      ,   'convert' : int},
                        'buff3'       : {'colName' : u'buff3'       ,   'convert' : int},
                        'parm3'       : {'colName' : u'param3'      ,   'convert' : int},
                    },
            },
       'C_RULES' : \
            {
               'fileName'   : u'all_rule_desc',
               'sheetName'  : u'client-all_rule_desc',
               'primeKey'   : u'id',
                'increment'  : True,
               'readOnlyCol': \
                    {
                        'PVP'              : {'colName' : u'PVP'          ,   'convert' : covertStr ,},
                        'HEAVEN_BATTLE'    : {'colName' : u'HEAVENBATTLE' ,   'convert' : covertStr ,},
                        'LOOT'             : {'colName' : u'LOOT'         ,   'convert' : covertStr ,},
                        'GREEDY'           : {'colName' : u'GREEDY'       ,   'convert' : covertStr ,},
                        'FARM_CLASH'       : {'colName' : u'FARMCLASH'    ,   'convert' : covertStr ,},
                        'DTFD'             : {'colName' : u'DTFD'         ,   'convert' : covertStr ,},
                        'MYSTICAL_LANDS'   : {'colName' : u'RELIC'        ,   'convert' : covertStr ,},
                        'DLC'              : {'colName' : u'DLC'          ,   'convert' : covertStr ,},
                        'GROUP'            : {'colName' : u'GROUP'        ,   'convert' : covertStr ,},
                        'GVE'              : {'colName' : u'GVE'          ,   'convert' : covertStr ,},
                        'WORLD_RELIC'      : {'colName' : u'WORLD_RELIC'  ,   'convert' : covertStr ,},
                        'COMPOSE'          : {'colName' : u'COMPOSE'      ,   'convert' : covertStr ,},
                        'MAZE'             : {'colName' : u'MAZE'         ,   'convert' : covertStr ,},
                        'DAILY_PVP'        : {'colName' : u'DAILY_PVP'    ,   'convert' : covertStr ,},
                        'GOLDEN_CITY'      : {'colName' : u'GOLDEN_CITY'  ,   'convert' : covertStr ,},
                        'PLAYER_EQUIP'     : {'colName' : u'PLAYER_EQUIP' ,   'convert' : covertStr ,},						
                        'AMBITION'         : {'colName' : u'AMBITION'     ,   'convert' : covertStr ,},	
						'TOWER'            : {'colName' : u'TOWER'        ,   'convert' : covertStr ,},	
						'PLANT'            : {'colName' : u'PLANT'        ,   'convert' : covertStr ,},	
                    },
            },
       'C_HERO_EXCLUSIVE' : \
            {
               'fileName'   : u'equipment',
               'sheetName'  : u'export-units_equip',
               'primeKey'   : u'same',
               'increment'  : True,
               'readOnlyCol': \
                    {
                        'equip_1'   : {'colName' : u'equip1'        ,   'convert' : int,},
                        'equip_2'   : {'colName' : u'equip2'        ,   'convert' : int,},
                        'equip_3'   : {'colName' : u'equip3'        ,   'convert' : int,},
                        'equip_4'   : {'colName' : u'equip4'        ,   'convert' : int,},
                        'equip_5'   : {'colName' : u'equip5'        ,   'convert' : int,},
                        'equip_6'   : {'colName' : u'equip6'        ,   'convert' : int,},
                    },
            },
        #攻略宝典配置
       'C_RAIDERS_KNOWLEDGE' : \
            {
               'fileName'   : u'knowledge',
               'sheetName'  : u'client-knowledge',
               'primeKey'   : u'id',
               'increment'  : True,#是否增量
               'readOnlyCol': \
                    {
                        'type'            : {'colName' : u'type'            ,   'convert' : int,},
                        'sort'            : {'colName' : u'sort'            ,   'convert' : int,},
                        'title'           : {'colName' : u'title'           ,   'convert' : covertStr ,},
                        'icon'            : {'colName' : u'icon'            ,   'convert' : covertStr ,},
                        'desc'            : {'colName' : u'desc'            ,   'convert' : covertStr ,},
                        'transmitdesc1'   : {'colName' : u'transmitdesc1'   ,   'convert' : covertStr ,},
                        'transmit1'       : {'colName' : u'transmit1'       ,   'convert' : covertStr ,},
                        'transmitdesc2'   : {'colName' : u'transmitdesc2'   ,   'convert' : covertStr ,},
                        'transmit2'       : {'colName' : u'transmit2'       ,   'convert' : covertStr ,},
                    },
            },
        #同门亲密度加成
       'C_FELLOW_INTIMACY' : \
            {
               'fileName'   : u'Team',
               'sheetName'  : u'export-intimacy',
               'primeKey'   : u'id',
               'increment'  : True,#是否增量
               'readOnlyCol': \
                    {
                        'intimacy': {'colName' : u'intimacy'  ,   'convert' : int,},
                        'atk_per' : {'colName' : u'atk_per'   ,   'convert' : int,},
                        'hp_per'  : {'colName' : u'hp_per'    ,   'convert' : int,},
                        'def_per' : {'colName' : u'def_per'   ,   'convert' : int,},
                        'cri'     : {'colName' : u'cri'       ,   'convert' : int,},
                        'eva'     : {'colName' : u'eva'       ,   'convert' : int,},
                        'reward'  : {'colName' : u'reward'    ,   'convert' : int,},
                    },
            },
        #攻略宝典配置
       'C_SUGGESTION' : \
            {
               'fileName'   : u'suggestion',
               'sheetName'  : u'client-suggestion',
               'primeKey'   : u'fbid',
               'increment'  : True,#是否增量
               'readOnlyCol': \
                    {
                        'monsterid'       : {'colName' : u'monsterid'       ,   'convert' : covertStr ,},
                    },
            },

        #xxxxx
       'C_HERO_FATE' : \
            {
               'fileName'   : u'karma',
               'sheetName'  : u'export-karma',
               'primeKey'   : u'id',
               'increment'  : True,#是否增量
               'readOnlyCol': \
                    {
                        'name'              : {'colName' : u'name'              ,   'convert' : covertStr ,},
                        'same'              : {'colName' : u'same'              ,   'convert' : int,},
                        'units1'            : {'colName' : u'units1'            ,   'convert' : int,},
                        'units2'            : {'colName' : u'units2'            ,   'convert' : int,},
                        'units3'            : {'colName' : u'units3'            ,   'convert' : int,},
                        'units4'            : {'colName' : u'units4'            ,   'convert' : int,},
                        'units5'            : {'colName' : u'units5'            ,   'convert' : int,},
                        'units6'            : {'colName' : u'units6'            ,   'convert' : int,},
                        'atk_per'           : {'colName' : u'atk_per'           ,   'convert' : int,},
                        'atk_abs'           : {'colName' : u'atk_abs'           ,   'convert' : int,},
                        'def_per'           : {'colName' : u'def_per'           ,   'convert' : int,},
                        'def_abs'           : {'colName' : u'def_abs'           ,   'convert' : int,},
                        'hp_per'            : {'colName' : u'hp_per'            ,   'convert' : int,},
                        'hp_abs'            : {'colName' : u'hp_abs'            ,   'convert' : int,},
                        'cri'               : {'colName' : u'cri'               ,   'convert' : float,},
                        'eva'               : {'colName' : u'eva'               ,   'convert' : float,},
                    },
            },
       'C_DLC_LIST' : \
            {
               'fileName'   : u'hero_dlc',
               'sheetName'  : u'export-Dlc_list',
               'primeKey'   : u'id',
               'increment'  : True,
               'readOnlyCol': \
                    {
                        'id'                : { 'colName' : u'id'                ,   'convert' : int, },
                        'name'              : { 'colName' : u'name'              ,   'convert' : covertStr , },
                        'background'        : { 'colName' : u'background'        ,   'convert' : covertStr , },
                        'scene_ids'         : { 'colName' : u'fb_ids'            ,   'convert' : covertStr , },
                        'scene_ids'         : { 'colName' : u'fb_ids'            ,   'convert' : covertStr , },
                        'namePath'          : { 'colName' : u'pname'             ,   'convert' : covertStr },
                    },
            },
       'C_DLC_FB' : \
            {
               'fileName'   : u'hero_dlc',
               'sheetName'  : u'export-Dlc_FbInfo',
               'primeKey'   : u'id',
               'increment'  : True,
               'readOnlyCol': \
                    {
                        'id'                : { 'colName' : u'id'                ,   'convert' : int, },
                        'type'              : { 'colName' : u'type'              ,   'convert' : int, },
                        'condition'         : { 'colName' : u'condition'         ,   'convert' : covertStr , },
                        'desc'              : { 'colName' : u'desc'              ,   'convert' : covertStr , },
                        'name'              : { 'colName' : u'name'              ,   'convert' : covertStr , },
                        'icon'              : { 'colName' : u'icon'              ,   'convert' : int, },
                        'cd_time'           : { 'colName' : u'cd_time'           ,   'convert' : int, },
                        'mask_name'         : { 'colName' : u'mask_name'         ,   'convert' : covertStr , },
                    },
            },

       'C_DLC_ACHIEVEMENT' : \
            {
               'fileName'   : u'hero_dlc',
               'sheetName'  : u'client-achievement',
               'primeKey'   : u'id',
               'increment'  : True,#是否增量
               'readOnlyCol': \
                    {
                        'type'              : {'colName' : u'type'              ,   'convert' : int,},
                        'star_num'          : {'colName' : u'star_num'          ,   'convert' : int,},
                        'desc'              : {'colName' : u'desc'              ,   'convert' : covertStr ,},
                        'dlc_num'           : {'colName' : u'dlc_num'           ,   'convert' : int,},
                    },
            },
       'C_ACHIEVEMENT' : \
            {
               'fileName'   : u'mission',
               'sheetName'  : u'export-missionpoint',
               'primeKey'   : u'id',
               'increment'  : True,#是否增量
               'readOnlyCol': \
                    {
                        'point'          : {'colName' : u'point'             ,   'convert' : int,},
                        'value'          : {'colName' : u'reward'            ,   'convert' : int,},
                        'pointtype'      : {'colName' : u'pointtype'         ,   'convert' : covertStr ,},
                        'desc'           : {'colName' : u'desc'              ,   'convert' : covertStr ,},
                    },
            },
       'C_COMPOSE_COST' : \
            {
               'fileName'   : u'compose',
               'sheetName'  : u'export-fusion',
               'primeKey'   : u'class',
               'increment'  : True,#是否增量
               'readOnlyCol': \
                    {
                        'cost_type'     : {'colName' : u'type'            ,   'convert' : int,},
                        'cost'          : {'colName' : u'cost'            ,   'convert' : int,},
                    },
            },
       'C_DECOMPOSE_COST' : \
            {
               'fileName'   : u'compose',
               'sheetName'  : u'export-refinery',
               'primeKey'   : u'class',
               'increment'  : True,#是否增量
               'readOnlyCol': \
                    {
                        'refinery_ret'  : {'colName' : u'type|itemid|amount1',   'convert' : covertStr,},
                        'soul_ret'      : {'colName' : u'type|itemid|amount2',   'convert' : covertStr,},
                        'scale_ret'     : {'colName' : u'scale'              ,   'convert' : float,},
                    },
            },
       'C_DECOMPOSE_REWARD' : \
            {
               'fileName'   : u'compose',
               'sheetName'  : u'export-base_refinery',
               'primeKey'   : u'id',
               'increment'  : True,#是否增量
               'readOnlyCol': \
                    {
                        'equ_gp_ret'   : {'colName' : u'equip_reward1',   'convert' : covertStr,},
                        'equ_soul_ret' : {'colName' : u'equip_reward2',   'convert' : covertStr,},
                        'mat_gp_ret'   : {'colName' : u'mat_reward1'  ,   'convert' : covertStr,},
                        'mat_soul_ret' : {'colName' : u'mat_reward2'  ,   'convert' : covertStr,},
                    },
            },

        'C_PET_SKILL_LIMIT' : \
            {
                'fileName'   : u'viplist',
                'sheetName'  : u'export-Vip',
                'primeKey'   : u'level',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'max_skill_point'           : {'colName' : u'skill_up_count',         'convert' : int},
                    },
            },

        'C_PET_LEVEL_UP_COST' : \
            {
                'fileName'   : u'Actor_Config',
                'sheetName'  : u'export-lvup_cost',
                'primeKey'   : u'lv',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'cost1'           : {'colName' : u'units_cost1',         'convert' : covertStr},
                        'cost2'           : {'colName' : u'units_cost2',         'convert' : covertStr},
                    },
            },

        'C_PET_SKILL_LEVEL_UP_COST' : \
            {
                'fileName'   : u'Actor_Config',
                'sheetName'  : u'export-lvup_cost',
                'primeKey'   : u'lv',
                'increment'  : True,
                'readOnlyCol': \
                    {
                        'cost_type1'           : {'colName' : u'skills_cost1',         'convert' : covertStr},
                        'cost_type2'           : {'colName' : u'skills_cost2',         'convert' : covertStr},
                        'cost_type3'           : {'colName' : u'skills_cost3',         'convert' : covertStr},
                        'cost_type4'           : {'colName' : u'skills_cost4',         'convert' : covertStr},
                        'cost_type5'           : {'colName' : u'skills_cost5',         'convert' : covertStr},
                    },
            },

       'C_EQUIPS'   : \
           {
               'fileName'   : u'equip',
               'sheetName'  : u'export-new_equip',
               'primeKey'   : u'id',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'name'         : {'colName' : u'name',           'convert' : covertStr },
                       'type'         : {'colName' : u'type',           'convert' : int },
                       'HP'           : {'colName' : u'init_hp',        'convert' : float },
                       'ATK'          : {'colName' : u'init_atk',       'convert' : float },
                       'DEF'          : {'colName' : u'init_def',       'convert' : float },
                       'EVA'          : {'colName' : u'init_dodge',     'convert' : float },
                       'CRI'          : {'colName' : u'init_cri',       'convert' : float },
                       'G_MATRL'      : {'colName' : u'gup_id',         'convert' : int },
                       'iconid'       : {'colName' : u'icon',           'convert' : int },
                       'pnum'         : {'colName' : u'piece_num',      'convert' : int },
                       'master_pet'   : {'colName' : u'units_same',     'convert' : int },
                       'desc'         : {'colName' : u'desc',           'convert' : covertStr },
                       'skill_choice' : {'colName' : u'skill_choice',   'convert' : int },
                   },
           },

       'C_EQUIP_STRENGTHEN'   : \
           {
               'fileName'   : u'equip',
               'sheetName'  : u'export-equip_strengthen',
               'primeKey'   : u'strengthen',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'level'        : {'colName' : u'level_need',     'convert' : int },
                       'addition'     : {'colName' : u'base_addition',  'convert' : int },
                       'success_rate' : {'colName' : u'success_rate',   'convert' : int },
                       'cost'         : {'colName' : u'cost',           'convert' : int },
                       'ret_level' : {'colName' : u'failed_level',   'convert' : int },
                   },
           },

       'C_PET_EQUIPS_ADVANCE_INFO'   : \
           {
               'fileName'   : u'equip',
               'sheetName'  : u'export-advanced',
               'primeKey'   : u'step',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'color'       : {'colName' : u'color',           'convert' : int },
                       'level'       : {'colName' : u'level',           'convert' : int },
                       'attr_mul'    : {'colName' : u'attr_mul',        'convert' : int },
                       'enchant_num' : {'colName' : u'enchant_num',     'convert' : int },
                       'step_show'   : {'colName' : u'step_show',       'convert' : int },
                       'cost'        : {'colName' : u'advanced_cost',   'convert' : int },
                       'skill_lvup'  : {'colName' : u'skill_lvup',      'convert' : int },
                   },
           },

       'C_PET_EQUIPS_ENCHANT_ATTR'   : \
           {
               'fileName'   : u'equip',
               'sheetName'  : u'export-adv_attr',
               'primeKey'   : u'id',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'color' : {'colName' : u'attr_color',   'convert' : int },
                       'type'  : {'colName' : u'attr_type',    'convert' : int },
                       'value' : {'colName' : u'attr_value',   'convert' : int },
                   },
           },

       'C_PET_EQUIPS_ADVANCE_MATRL'   : \
           {
               'fileName'   : u'equip',
               'sheetName'  : u'export-equip_gup',
               'primeKey'   : u'id',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'step_1'  : {'colName' : u'gup1' ,   'convert' : covertStr },
                       'step_2'  : {'colName' : u'gup2' ,   'convert' : covertStr },
                       'step_3'  : {'colName' : u'gup3' ,   'convert' : covertStr },
                       'step_4'  : {'colName' : u'gup4' ,   'convert' : covertStr },
                       'step_5'  : {'colName' : u'gup5' ,   'convert' : covertStr },
                       'step_6'  : {'colName' : u'gup6' ,   'convert' : covertStr },
                       'step_7'  : {'colName' : u'gup7' ,   'convert' : covertStr },
                       'step_8'  : {'colName' : u'gup8' ,   'convert' : covertStr },
                       'step_9'  : {'colName' : u'gup9' ,   'convert' : covertStr },
                       'step_10' : {'colName' : u'gup10',   'convert' : covertStr },
                       'step_11' : {'colName' : u'gup11',   'convert' : covertStr },
                       'step_12' : {'colName' : u'gup12',   'convert' : covertStr },
                       'step_13' : {'colName' : u'gup13',   'convert' : covertStr },
                       'step_14' : {'colName' : u'gup14',   'convert' : covertStr },
                       'step_15' : {'colName' : u'gup15',   'convert' : covertStr },
                       'step_16' : {'colName' : u'gup16',   'convert' : covertStr },
                       'step_17' : {'colName' : u'gup17',   'convert' : covertStr },
                       'step_18' : {'colName' : u'gup18',   'convert' : covertStr },
                       'step_19' : {'colName' : u'gup19',   'convert' : covertStr },
                       'step_20' : {'colName' : u'gup20',   'convert' : covertStr },
                   },
           },

       'C_DUEL_EMENY'   : \
           {
               'fileName'   : u'duel',
               'sheetName'  : u'client-duel',
               'primeKey'   : u'duel_fb',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'npc_model'  : {'colName' : u'enemy_npc' ,   'convert' : covertStr },
                       'pet_model'  : {'colName' : u'enemy_unit' ,  'convert' : covertStr },
                   },
           },

       'C_DUEL_PLAYER_NPC'   : \
            {
               'fileName'   : u'duel',
               'sheetName'  : u'client-head',
               'primeKey'   : u'item_head',
                'increment'  : True,
                'readOnlyCol': \
                    {
                       'npc_model'  : {'colName' : u'player_npc' ,   'convert' : covertStr },
                    },
            },

       'C_LIGHT_NORMAL'   : \
           {
               'fileName'   : u'HeroGrowth',
               'sheetName'  : u'export-ambition',
               'primeKey'   : u'id',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'open_level'    : {'colName' : u'open_level'   ,   'convert' : int },
                       'attr_type'     : {'colName' : u'attr_type'    ,   'convert' : int },
                       #  'cost'          : {'colName' : u'cost'         ,   'convert' : int },
                       #  'success_rate'  : {'colName' : u'success_rate' ,   'convert' : int },
                       #  'addition'      : {'colName' : u'addition'     ,   'convert' : covertStr },
                   },
           },

       'C_LIGHT_VIP'   : \
           {
               'fileName'   : u'HeroGrowth',
               'sheetName'  : u'export-vip_ambition',
               'primeKey'   : u'id',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'open_level'    : {'colName' : u'open_level'   ,   'convert' : int },
                       'attr_type'     : {'colName' : u'attr_type'    ,   'convert' : int },
                       #  'cost'          : {'colName' : u'cost'         ,   'convert' : int },
                       #  'success_rate'  : {'colName' : u'success_rate' ,   'convert' : int },
                       #  'addition'      : {'colName' : u'addition'     ,   'convert' : covertStr },
                   },
           },
       'C_LIGHT_VALUE'   : \
           {
               'fileName'   : u'HeroGrowth',
               'sheetName'  : u'export-random_ambition',
               'primeKey'   : u'step',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'ATK'    : {'colName' : u'atk'   ,   'convert' : float },
                       'DEF'    : {'colName' : u'def'   ,   'convert' : float },
                       'HP'     : {'colName' : u'hp'    ,   'convert' : float },
                       'EVA'    : {'colName' : u'doge'  ,   'convert' : float },
                       'CRI'    : {'colName' : u'cri'   ,   'convert' : float },
                   },
           },
       'C_LIGHT_PIC'   : \
           {
               'fileName'   : u'HeroGrowth',
               'sheetName'  : u'client-ambition_page',
               'primeKey'   : u'group',
               'sliceKey'   : u'type', #导出的名字
               'sliceConfig': {
                   'NORMAL'  : {'sliceFunc': lambda x: x == 1.0},
                   'VIP'     : {'sliceFunc': lambda x: x == 2.0},
                   },
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'type'          : {'colName' : u'open_type'    ,   'convert' : covertStr },
                       'npc_pic'       : {'colName' : u'npc_pic'      ,   'convert' : covertStr },
                       'name_pic'      : {'colName' : u'name_pic'     ,   'convert' : covertStr },
                   },
           },

       'C_PET_EXCHANGE_COST'   : \
           {
               'fileName'   : u'compose',
               'sheetName'  : u'export-pet_exchange_cost',
               'primeKey'   : u'class',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'cost'           : {'colName' : u'cost'          ,   'convert' : int },
                       'cost_type'      : {'colName' : u'type'          ,   'convert' : int },
                   },
           },

       'C_PLAYER_EQUIP'   : \
           {
               'fileName'   : u'equip',
               'sheetName'  : u'export-player_equip',
               'primeKey'   : u'id',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'cost'           : {'colName' : u'cost_mul'      ,   'convert' : int },
                       'icon'           : {'colName' : u'icon'          ,   'convert' : covertStr },
                       'gem_group'      : {'colName' : u'gem_group'     ,   'convert' : covertStr },
                   },
           },

       'C_PLAYER_COST'   : \
           {
               'fileName'   : u'equip',
               'sheetName'  : u'export-pequip_strengthen',
               'primeKey'   : u'level',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'addition'       : {'colName' : u'base_addition'      ,   'convert' : int },
                       'cost'           : {'colName' : u'base_cost'          ,   'convert' : int },
                   },
           },

       'C_PLANT_SEED'   : \
           {
               'fileName'   : u'campaign',
               'sheetName'  : u'export-plant',
               'primeKey'   : u'seed_id',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'attr'    : {'colName' : u'attr'                     ,   'convert' : int },
                       'reward1' : {'colName' : u'type|itemID|amount1'      ,   'convert' : covertStr },
                       'reward2' : {'colName' : u'type|itemID|amount2'      ,   'convert' : covertStr },
                       'reward3' : {'colName' : u'type|itemID|amount3'      ,   'convert' : covertStr },
                       'reward4' : {'colName' : u'type|itemID|amount4'      ,   'convert' : covertStr },
                       'reward5' : {'colName' : u'type|itemID|amount5'      ,   'convert' : covertStr },
                       'reward6' : {'colName' : u'type|itemID|amount6'      ,   'convert' : covertStr },
                       'reward7' : {'colName' : u'type|itemID|amount7'      ,   'convert' : covertStr },
                       'reward8' : {'colName' : u'type|itemID|amount8'      ,   'convert' : covertStr },
                   },
           },

       'C_HONOR_INFO'   : \
           {
               'fileName'   : u'mission',
               'sheetName'  : u'export-glory',
               'primeKey'   : u'id',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'campaignid'      : {'colName' : u'campaignid'                     ,   'convert' : int },
                       'planvalue'       : {'colName' : u'planvalue'                      ,   'convert' : int },
                       'addition_1'      : {'colName' : u'reward1'                        ,   'convert' : int },
                       'addition_2'      : {'colName' : u'reward2'                        ,   'convert' : int },
                       'addition_type_1' : {'colName' : u'pointtype1'                     ,   'convert' : covertStr },
                       'addition_type_2' : {'colName' : u'pointtype2'                     ,   'convert' : covertStr },
                       'desc'            : {'colName' : u'desc'                           ,   'convert' : covertStr },
                       'title'           : {'colName' : u'titledesc'                      ,   'convert' : covertStr },
                   },
           },

       'C_GOLDEN_MONSTER'   : \
           {
               'fileName'   : u'golden_city',
               'sheetName'  : u'export-golden_monstergroup',
               'primeKey'   : u'id',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'monster_star'          : {'colName' : u'monster_star'              ,   'convert' : int },
                       'monster_id1'           : {'colName' : u'monster_id1'               ,   'convert' : int },
                       'monster_id2'           : {'colName' : u'monster_id2'               ,   'convert' : int },
                       'monster_id3'           : {'colName' : u'monster_id3'               ,   'convert' : int },
                       'monster_id4'           : {'colName' : u'monster_id4'               ,   'convert' : int },
                       'monster_group_count'   : {'colName' : u'monster_group_count'       ,   'convert' : int },
                   },
           },

       'C_GEM'   : \
           {
               'fileName'   : u'gem',
               'sheetName'  : u'export-gem',
               'primeKey'   : u'id',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'type'              : {'colName' : u'type'              ,   'convert' : int },
                       'step'              : {'colName' : u'step'              ,   'convert' : int },
                       'gupr'              : {'colName' : u'gupr'              ,   'convert' : int },
                       'compose_need_num'  : {'colName' : u'compose_need_num'  ,   'convert' : int },
                       'icon'              : {'colName' : u'icon'              ,   'convert' : int },
                       'name'              : {'colName' : u'name'              ,   'convert' : covertStr },
                       'desc'              : {'colName' : u'desc'              ,   'convert' : covertStr },
                       'atk'               : {'colName' : u'atk'               ,   'convert' : int },
                       'hp'                : {'colName' : u'hp'                ,   'convert' : int },
                       'def'               : {'colName' : u'def'               ,   'convert' : int },
                   },
           },

       'C_GEM_REFINING'   : \
           {
               'fileName'   : u'gem',
               'sheetName'  : u'export-refining',
               'primeKey'   : u'refining_lv',
               'increment'  : True,
               'readOnlyCol': \
                   {
                       'gem_lv_limit'  : {'colName' : u'gem_lv_limit'  ,   'convert' : int },
                       'cost'          : {'colName' : u'cost'          ,   'convert' : int },
                       'cost_type'     : {'colName' : u'cost_type'     ,   'convert' : int },
                       'color'         : {'colName' : u'color'         ,   'convert' : int },
                       'step'          : {'colName' : u'step'          ,   'convert' : int },
                   },
           },
    }

