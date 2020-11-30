from pdfrw import PdfReader, PdfWriter, PdfDict, PdfObject, objects as pdfrw_objects
from io import BytesIO
from pathlib import Path

default_options = {
    "template": "default.pdf"
}

def populateSheet(character, context, options=default_options):
    pdfPath = Path(context.function_directory)
    pdf = PdfReader(pdfPath / options['template'])
    pdf.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject('true')))

    populateFields(character, pdf.Root.AcroForm.Fields)

    output = BytesIO()
    PdfWriter().write(output, pdf)
    output.seek(0)
    return output.read()

def getCheckBoxValue(value):
    return pdfrw_objects.pdfname.BasePdfName('/Yes' if value else "/No")

def getSkillMod(modifier, is_proficient=False, prof_bonus=0):
    skill_mod = modifier + (prof_bonus if is_proficient else 0)
    return F"{'+' if skill_mod >=0 else ''}{skill_mod}"

def populateFields(character, fields):
    #general
    fields[0].V = F"{character['class']['name']} ({character['subclass']['name']}) {str(character['level'])}"
    fields[3].V = character['name']
    if('subrace' in character):
        fields[4]=F"{character['race']['name']} ({character['subrace']['name']})"
    else:
        fields[4].V = character['race']['name']
    fields[5].V = character['alignment']
    fields[9].V = str(character['prof_bonus'])
    fields[11].V = getSkillMod(character['stats']['dex']['modifier'])
    fields[12].V = F"{character['base_speed']}ft"
    fields[24].V = F"{character['level']}d{character['hit_die']}"
    fields[97].V = str(10 + character['stats']['wis']['modifier'] + (character['prof_bonus'] if character['skills']['perception']['proficient'] else 0))
    fields[99].V = ', '.join([prof['name'] for prof in character['proficiencies']]) + '\n\n' + ', '.join([lang['name'] for lang in character['languages']])
    fields[105].V = '\n\n'.join([F"{feat['name']}: {' '.join(feat['desc'])}" for feat in character['features']])

    ## stats totals
    fields[8].V = str(character['stats']['str']['total'])
    fields[17].V = str(character['stats']['dex']['total'])
    fields[23].V = str(character['stats']['con']['total'])
    fields[34].V = str(character['stats']['int']['total'])
    fields[61].V = str(character['stats']['wis']['total'])
    fields[68].V = str(character['stats']['cha']['total'])
    ## stats modifiers
    fields[14].V = getSkillMod(character['stats']['str']['modifier'])
    fields[20].V = getSkillMod(character['stats']['dex']['modifier'])
    fields[28].V = getSkillMod(character['stats']['con']['modifier'])
    fields[56].V = getSkillMod(character['stats']['int']['modifier'])
    fields[67].V = getSkillMod(character['stats']['wis']['modifier'])
    fields[94].V = getSkillMod(character['stats']['cha']['modifier'])
    #save proficiencies
    fields[47].V = getCheckBoxValue(character['saves']['str']['proficient'])
    fields[48].V = getCheckBoxValue(character['saves']['dex']['proficient'])
    fields[49].V = getCheckBoxValue(character['saves']['con']['proficient'])
    fields[50].V = getCheckBoxValue(character['saves']['int']['proficient'])
    fields[51].V = getCheckBoxValue(character['saves']['wis']['proficient'])
    fields[52].V = getCheckBoxValue(character['saves']['cha']['proficient'])
    fields[47].AS = getCheckBoxValue(character['saves']['str']['proficient'])
    fields[48].AS = getCheckBoxValue(character['saves']['dex']['proficient'])
    fields[49].AS = getCheckBoxValue(character['saves']['con']['proficient'])
    fields[50].AS = getCheckBoxValue(character['saves']['int']['proficient'])
    fields[51].AS = getCheckBoxValue(character['saves']['wis']['proficient'])
    fields[52].AS = getCheckBoxValue(character['saves']['cha']['proficient'])
    #save modifiers
    fields[16].V = getSkillMod(character['stats']['str']['modifier'], character['saves']['str']['proficient'], character['prof_bonus'])
    fields[35].V = getSkillMod(character['stats']['dex']['modifier'], character['saves']['dex']['proficient'], character['prof_bonus'])
    fields[36].V = getSkillMod(character['stats']['con']['modifier'], character['saves']['con']['proficient'], character['prof_bonus'])
    fields[37].V = getSkillMod(character['stats']['int']['modifier'], character['saves']['int']['proficient'], character['prof_bonus'])
    fields[38].V = getSkillMod(character['stats']['wis']['modifier'], character['saves']['wis']['proficient'], character['prof_bonus'])
    fields[39].V = getSkillMod(character['stats']['cha']['modifier'], character['saves']['cha']['proficient'], character['prof_bonus'])

    #skill modifiers
    fields[40].V = getSkillMod(character['stats']['dex']['modifier'], character['skills']['acrobatics']['proficient'], character['prof_bonus'])
    fields[41].V = getSkillMod(character['stats']['wis']['modifier'], character['skills']['animal-handling']['proficient'], character['prof_bonus'])
    fields[42].V = getSkillMod(character['stats']['str']['modifier'], character['skills']['athletics']['proficient'], character['prof_bonus'])
    fields[43].V = getSkillMod(character['stats']['cha']['modifier'], character['skills']['deception']['proficient'], character['prof_bonus'])
    fields[44].V = getSkillMod(character['stats']['int']['modifier'], character['skills']['history']['proficient'], character['prof_bonus'])
    fields[45].V = getSkillMod(character['stats']['wis']['modifier'], character['skills']['insight']['proficient'], character['prof_bonus'])
    fields[46].V = getSkillMod(character['stats']['cha']['modifier'], character['skills']['intimidation']['proficient'], character['prof_bonus'])
    fields[60].V = getSkillMod(character['stats']['int']['modifier'], character['skills']['investigation']['proficient'], character['prof_bonus'])
    fields[64].V = getSkillMod(character['stats']['int']['modifier'], character['skills']['arcana']['proficient'], character['prof_bonus'])
    fields[66].V = getSkillMod(character['stats']['wis']['modifier'], character['skills']['perception']['proficient'], character['prof_bonus'])
    fields[69].V = getSkillMod(character['stats']['int']['modifier'], character['skills']['nature']['proficient'], character['prof_bonus'])
    fields[70].V = getSkillMod(character['stats']['cha']['modifier'], character['skills']['performance']['proficient'], character['prof_bonus'])
    fields[71].V = getSkillMod(character['stats']['wis']['modifier'], character['skills']['medicine']['proficient'], character['prof_bonus'])
    fields[72].V = getSkillMod(character['stats']['int']['modifier'], character['skills']['religion']['proficient'], character['prof_bonus'])
    fields[73].V = getSkillMod(character['stats']['dex']['modifier'], character['skills']['stealth']['proficient'], character['prof_bonus'])
    fields[92].V = getSkillMod(character['stats']['cha']['modifier'], character['skills']['persuasion']['proficient'], character['prof_bonus'])
    fields[93].V = getSkillMod(character['stats']['dex']['modifier'], character['skills']['sleight-of-hand']['proficient'], character['prof_bonus'])
    fields[95].V = getSkillMod(character['stats']['wis']['modifier'], character['skills']['survival']['proficient'], character['prof_bonus'])

    #skill proficiencies
    fields[74].V = getCheckBoxValue(character['skills']['acrobatics']['proficient'])
    fields[75].V = getCheckBoxValue(character['skills']['animal-handling']['proficient'])
    fields[76].V = getCheckBoxValue(character['skills']['arcana']['proficient'])
    fields[77].V = getCheckBoxValue(character['skills']['athletics']['proficient'])
    fields[78].V = getCheckBoxValue(character['skills']['deception']['proficient'])
    fields[79].V = getCheckBoxValue(character['skills']['history']['proficient'])
    fields[80].V = getCheckBoxValue(character['skills']['insight']['proficient'])
    fields[81].V = getCheckBoxValue(character['skills']['intimidation']['proficient'])
    fields[82].V = getCheckBoxValue(character['skills']['investigation']['proficient'])
    fields[83].V = getCheckBoxValue(character['skills']['medicine']['proficient'])
    fields[84].V = getCheckBoxValue(character['skills']['nature']['proficient'])
    fields[85].V = getCheckBoxValue(character['skills']['perception']['proficient'])
    fields[86].V = getCheckBoxValue(character['skills']['performance']['proficient'])
    fields[87].V = getCheckBoxValue(character['skills']['persuasion']['proficient'])
    fields[88].V = getCheckBoxValue(character['skills']['religion']['proficient'])
    fields[89].V = getCheckBoxValue(character['skills']['sleight-of-hand']['proficient'])
    fields[90].V = getCheckBoxValue(character['skills']['stealth']['proficient'])
    fields[91].V = getCheckBoxValue(character['skills']['survival']['proficient'])
    fields[74].AS = getCheckBoxValue(character['skills']['acrobatics']['proficient'])
    fields[75].AS = getCheckBoxValue(character['skills']['animal-handling']['proficient'])
    fields[76].AS = getCheckBoxValue(character['skills']['arcana']['proficient'])
    fields[77].AS = getCheckBoxValue(character['skills']['athletics']['proficient'])
    fields[78].AS = getCheckBoxValue(character['skills']['deception']['proficient'])
    fields[79].AS = getCheckBoxValue(character['skills']['history']['proficient'])
    fields[80].AS = getCheckBoxValue(character['skills']['insight']['proficient'])
    fields[81].AS = getCheckBoxValue(character['skills']['intimidation']['proficient'])
    fields[82].AS = getCheckBoxValue(character['skills']['investigation']['proficient'])
    fields[83].AS = getCheckBoxValue(character['skills']['medicine']['proficient'])
    fields[84].AS = getCheckBoxValue(character['skills']['nature']['proficient'])
    fields[85].AS = getCheckBoxValue(character['skills']['perception']['proficient'])
    fields[86].AS = getCheckBoxValue(character['skills']['performance']['proficient'])
    fields[87].AS = getCheckBoxValue(character['skills']['persuasion']['proficient'])
    fields[88].AS = getCheckBoxValue(character['skills']['religion']['proficient'])
    fields[89].AS = getCheckBoxValue(character['skills']['sleight-of-hand']['proficient'])
    fields[90].AS = getCheckBoxValue(character['skills']['stealth']['proficient'])
    fields[91].AS = getCheckBoxValue(character['skills']['survival']['proficient'])

