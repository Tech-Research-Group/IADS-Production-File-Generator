"""WORK PACKAGE CONVERTER"""
from tkinter import filedialog, messagebox
import tkinter.font as tkfont
from tkinter.scrolledtext import ScrolledText
import datetime
import os
import re
import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, BOTTOM, END, FALSE, LEFT, RIGHT, TOP, TRUE, WORD, X, YES


def get_date():
    """Gets the current publication date in proper TM format."""
    date = datetime.datetime.now()
    day = date.day
    month = date.month
    year = date.year
    if month == 1:
        month_name = "JANUARY"
    elif month == 2:
        month_name = "FEBRUARY"
    elif month == 3:
        month_name = "MARCH"
    elif month == 4:
        month_name = "APRIL"
    elif month == 5:
        month_name = "MAY"
    elif month == 6:
        month_name = "JUNE"
    elif month == 7:
        month_name = "JULY"
    elif month == 8:
        month_name = "AUGUST"
    elif month == 9:
        month_name = "SEPTEMBER"
    elif month == 10:
        month_name = "OCTOBER"
    elif month == 11:
        month_name = "NOVEMBER"
    elif month == 12:
        month_name = "DECEMBER"

    return f'{day} {month_name} {year}'


def get_wp_code(filename) -> str:
    """Grabs WP code from filename."""
    # wp_code = re.findall(r"(\w\d+)", filename)
    return re.findall(r"(\w\d+)", filename)[1]

def open_wip_dir() -> None:
    """Opens TM WIP folder and creates a production.xml file an IADS project."""
    # attributes: list[str] = []
    XML_VERSION = '<?xml version="1.0" encoding="UTF-8"?>'
    DOCTYPE_OPEN = '<!DOCTYPE production PUBLIC "-//USA-DOD//DTD -1/2D TM Assembly REV D 7.0 20220130//EN" "../dtd/40051D_7_0.dtd" ['
    DOCTYPE_CLOSE = ']>'
    production_tag = f'<production date="1 JUNE 2023" chnglevel="0" chngdate="{get_date()}" pin="XX-XXXX-XXX-XX">'
    paper_frnt_tag = '<paper.frnt> '
    gim_entities = ''
    opim_entities = ''
    usual_entities = ''
    unusual_entities = ''
    tsim_entities = ''
    tim_entities = ''
    mtim_entities = ''
    mim_entities = ''
    mim2_entities = ''
    omim_entities = ''
    mmim_entities = ''
    dim_entities = ''
    sim_entities = ''
    pim_entities = ''
    rear_entity = ''
    production_xml = f'{XML_VERSION}\n{DOCTYPE_OPEN}\n'
    _c = 0
    _o = 0
    _u = 0

    if filenames := filedialog.askopenfilenames():
        for path in filenames:
            filename = os.path.basename(path)
            
            if "entitydeclaration" in filename.lower():
                continue
            elif "front cover" in filename.lower() or "title page" in filename.lower():
                tag = "frntcover"
                paper_frnt_tag += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'

                with open(path, 'r', encoding='utf-8') as _f:
                    for line in _f:
                        if "<name>" in line:
                            system_name = line.lstrip('\t')[6:-8]
                            # system_name = line.lstrip('(')[0]
                            # system_abbr = system_name[1][:-2]
                    _f.close()
            elif "warning" in filename.lower() or "summary" in filename.lower():
                tag = "warnsum"
                paper_frnt_tag += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "loep" in filename.lower() or "effective" in filename.lower():
                tag = "loep"
                paper_frnt_tag += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "titleblock_toc_howtouse" in filename.lower():
                tag = "tb_toc_htu"
                paper_frnt_tag += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "howtouse" in filename.lower() or "how_to_use" in filename.lower():
                tag = "howtouse"
                paper_frnt_tag += f'&{tag};\n\t'
                production_xml += f'\t{get_entity_data(tag, filename)}'
                
            # GENERAL INFORMATION, EQUIPMENT DESCRIPTION, and THEORY OF OPERATIONS
            elif "general info" in filename.lower() or "geninfo" in filename.lower() or "generalinfo" in filename.lower() or "gen_info" in filename.lower() or "general_info" in filename.lower() and "chap" not in filename.lower() and "start" not in filename.lower() and "end" not in filename.lower():
                tag = "ginfowp"
                gim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "equipment" in filename.lower() and "description" in filename.lower():
                tag = "descwp"
                gim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "theoryops" in filename.lower() or "theoryofop" in filename.lower() or "thryops" in filename.lower() or "theory" in filename.lower():
                tag = "thrywp"
                gim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            
            # OPERATOR INSTRUCTIONS
            elif "controls" in filename.lower() and "indicators" in filename.lower():
                if opim_entities == "":
                    tag = "ctrlindwp"
                    opim_entities += f'&{tag}; '
                else:
                    _c += 1
                    tag = f"ctrlindwp{_c}"
                    opim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "O00" in filename and "unusual" not in filename.lower():
                if usual_entities == "":
                    tag = "opusualwp"
                    usual_entities += f'&{tag}; '
                else:
                    _o += 1
                    tag = f"opusualwp{_o}"
                    usual_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "O00" in filename and "unusual" in filename.lower():
                if unusual_entities == "":
                    tag = "opunuwp"
                    unusual_entities += f'&{tag}; '
                else:
                    _u += 1
                    tag = f"opunuwp{_u}"
                    unusual_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'

            # TROUBLESHOOTING MASTER INDEX
            elif "TSMasterIndex" in filename:
                tag = "tsmasterwp"
                tsim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'

            # TROUBLESHOOTING
            elif ("TS" in filename or "troubleshooting" in filename.lower()) and "intro" in filename.lower():
                tag = "tsintrowp"
                with open(path, "r", encoding="utf-8") as _f:
                    for line in _f:
                        line = line.lstrip("\t")
                        if "<maintlvl level=" in line and "operator" in line:
                            print(line)
                            tag = f'{tag}-oper'
                            tim_entities += f'&{tag}; '
                        elif "<maintlvl level=" in line and "maintainer" in line:
                            print(line)
                            tag = f'{tag}-main'
                            mtim_entities += f'&{tag}; '
                    _f.close()
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif ("TS" in filename or "troubleshooting" in filename.lower()) and "index" in filename.lower():
                tag = "tsindexwp"
                with open(path, "r", encoding="utf-8") as _f:
                    for line in _f:
                        line = line.lstrip("\t")
                        if "<maintlvl level" in line and "operator" in line:
                            tag = f'{tag}-oper'
                            tim_entities += f'&{tag}; '
                        elif "<maintlvl level" in line and "maintainer" in line:
                            tag = f'{tag}-main'
                            mtim_entities += f'&{tag}; '
                    _f.close()
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "T000" in filename and "intro" not in filename.lower() and "index" not in filename.lower() and "start" not in filename.lower() and "end" not in filename.lower() and "chap" not in filename.lower():
                tag = get_wp_code(filename)
                tim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "T001" in filename and "intro" not in filename.lower() and "index" not in filename.lower() and "start" not in filename.lower() and "end" not in filename.lower() and "chap" not in filename.lower():
                tag = get_wp_code(filename)
                mtim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'

            # PREVENTIVE MAINTENANCE CHECKS AND SERVICES (PMCS)
            elif "M00" in filename and "PMCS" in filename and "intro" in filename.lower():
                tag = "pmcsintrowp"
                with open(path, "r", encoding="utf-8") as _f:
                    for line in _f:
                        line = line.lstrip("\t")
                        if "<maintlvl level" in line and "operator" in line:
                            tag = f'{tag}-oper'
                            mim_entities += f'&{tag}; '
                        elif "<maintlvl level" in line and "maintainer" in line:
                            tag = f'{tag}-main'
                            mim2_entities += f'&{tag}; '
                    _f.close()
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "M000" in filename and "PMCS" in filename and "daily" in filename.lower() or "weekly" in filename.lower() or "monthly" in filename.lower() or "quarterly" in filename.lower() or "semi-annually" in filename.lower() or "annually" in filename.lower() or "before" in filename.lower() or "during" in filename.lower() or "after" in filename.lower():
                tag = get_wp_code(filename)
                mim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif ("M001" in filename or "M002" in filename) and "PMCS" in filename and "daily" in filename.lower() or "weekly" in filename.lower() or "monthly" in filename.lower() or "quarterly" in filename.lower() or "semi-annually" in filename.lower() or "annually" in filename.lower() or "before" in filename.lower() or "during" in filename.lower() or "after" in filename.lower():
                tag = get_wp_code(filename)
                mim2_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'

            # MAINTENANCE PROCEDURES
            elif "M000" in filename and "PMCS" not in filename:
                tag = get_wp_code(filename)
                omim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif ("M001" in filename or "M002" in filename) and "PMCS" not in filename:
                tag = get_wp_code(filename)
                mmim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'

            # DESTRUCTION OF EQUIPMENT TO PREVENT ENEMY USE
            elif "D00" in filename and "intro" in filename.lower() and "destruct" in filename.lower():
                tag = "destruct-introwp"
                dim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "D00" in filename and "Intro" not in filename.lower():
                tag = get_wp_code(filename)
                dim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'

            # REPAIR PARTS AND SPECIAL TOOLS LIST (RPSTL)
            elif "rpstl" in filename.lower() and "intro" in filename.lower() and "start" not in filename.lower() and "end" not in filename.lower():
                tag = "introwp"
                pim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "R00" in filename and "intro" not in filename.lower() and "nsn" not in filename.lower() and "pn" not in filename.lower() and "bulk" not in filename.lower() and "partnumber" not in filename.lower() and "index" not in filename.lower() and "start" not in filename.lower() and "end" not in filename.lower():
                tag = get_wp_code(filename)
                pim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "R00" in filename and "bulk" in filename.lower() and "item" in filename.lower():
                tag = "bulk_itemswp"
                pim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "R00" in filename and "NSN" in filename and "index" in filename.lower():
                tag = "nsnindxwp"
                pim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "R00" in filename and "PN" in filename or "part" in filename.lower() and "index" in filename.lower():
                tag = "pnindxwp"
                pim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'

            # SUPPORTING INFORMATION
            elif "S00" in filename and "reference" in filename.lower():
                tag = "refwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "S00" in filename and "mac" in filename.lower() and "intro" in filename.lower():
                tag = "macintrowp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "S00" in filename and "mac" in filename.lower() and "intro" not in filename.lower():
                tag = "macwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "S00" in filename and "COEI" in filename or "BII" in filename:
                tag = "coeibiiwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "S00" in filename and "expendable" in filename.lower() or "durable" in filename.lower() or "EDIL" in filename:
                tag = "explistwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "S00" in filename and "AAL" in filename or "additional" in filename.lower() and "authorization" in filename.lower():
                tag = "aalwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "S00" in filename and "TIL" in filename or "tool" in filename.lower() and "identification" in filename.lower():
                tag = "tilwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "S00" in filename and "MRP" in filename or "mandatory" in filename.lower() and "replacement" in filename.lower():
                tag = "mrplwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "S00" in filename and "CSI" in filename or "critical" in filename.lower() and "safety" in filename.lower():
                tag = "csi.wp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "S00" in filename and "support" in filename.lower() and "item" in filename.lower():
                tag = "supitemwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "S00" in filename and "additional" in filename.lower() and "supporting" in filename.lower():
                tag = "genwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            
            # REAR MATTER
            elif "rear" in filename.lower() and "matter" in filename.lower():
                tag = "rear"
                rear_entity += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
                break
    
    print("ENTITIES IN WIP FOLDER")
    # Concatenate XML file by tags/sections
    # paper_manual_tag = f'<paper.manual maintitl="{attributes[2]}" maintlvls="{attributes[1]}" revno="0" rpstl="{attributes[3]}" pubno="{attributes[0]}">'
    paper_manual_tag = '<paper.manual maintitl="" maintlvls="" revno="0" rpstl="" pubno="">'
    production_xml += f'{DOCTYPE_CLOSE}\n{production_tag}\n\t{paper_manual_tag}\n\t\t{paper_frnt_tag}\n\t\t</paper.frnt>\n'
    print(paper_frnt_tag)
    production_xml += f'\t\t<gim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>{system_name}</name>\n\t\t\t</titlepg>\n'
    production_xml += f'\t\t\t{gim_entities}\n\t\t</gim>\n'
    print(gim_entities)
    if opim_entities != '':
        production_xml += f'\t\t<opim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>{system_name}</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t{opim_entities}{usual_entities}{unusual_entities}\n\t\t</opim>\n'
        print(f'{opim_entities} {usual_entities} {unusual_entities}')
    if tsim_entities != '':
        production_xml += f'\t\t<tim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>{system_name}</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t<masterindexcategory>\n\t\t\t\t{tsim_entities}\n\t\t\t</masterindexcategory>\n\t\t</tim>\n'
        print(tsim_entities)
    if tim_entities != '':
        production_xml += f'\t\t<tim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>{system_name}</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t<troublecategory>\n\t\t\t\t{tim_entities}\n\t\t\t</troublecategory>\n\t\t</tim>\n'
        print(tim_entities)
    if mtim_entities != '':
        production_xml += f'\t\t<tim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="maintainer">\n\t\t\t\t<name>{system_name}</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t<troublecategory>\n\t\t\t\t{mtim_entities}\n\t\t\t</troublecategory>\n\t\t</tim>\n'
        print(mtim_entities)
    if mim_entities != '':
        production_xml += f'\t\t<mim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>{system_name}</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t<pmcscategory>\n\t\t\t\t{mim_entities}\n\t\t\t</pmcscategory>\n\t\t</mim>\n'
        print(mim_entities)
    if mim2_entities != '':
        production_xml += f'\t\t<mim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="maintainer">\n\t\t\t\t<name>{system_name}</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t<pmcscategory>\n\t\t\t\t{mim2_entities}\n\t\t\t</pmcscategory>\n\t\t</mim>\n'
        print(mim2_entities)
    if omim_entities != '':
        production_xml += f'\t\t<mim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>{system_name}</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t<maintenancecategory>\n\t\t\t\t{omim_entities}\n\t\t\t</maintenancecategory>\n\t\t</mim>\n'
        print(omim_entities)
    if mmim_entities != '':
        production_xml += f'\t\t<mim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="maintainer">\n\t\t\t\t<name>{system_name}</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t<maintenancecategory>\n\t\t\t\t{mmim_entities}\n\t\t\t</maintenancecategory>\n\t\t</mim>\n'
        print(mmim_entities)
    if dim_entities != '':
        production_xml += f'\t\t<dim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>{system_name}</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t{dim_entities}\n\t\t</dim>\n'
        print(dim_entities)
    if pim_entities != '':
        production_xml += f'\t\t<pim chngno="0" dmwr-inclus="none" revno="0" chap-toc="no">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>{system_name}</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t{pim_entities}\n\t\t</pim>\n'
        print(pim_entities)
    if sim_entities != '':
        production_xml += f'\t\t<sim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>{system_name}</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t{sim_entities}\n\t\t</sim>\n'
        print(sim_entities)
    
    if rear_entity != '':
        production_xml += f'\t\t{rear_entity}\n'
        print(rear_entity)
    production_xml += '\t</paper.manual>\n</production>'
    textbox.insert(END, production_xml)
    save_btn.configure(state="normal")


def get_entity_data(tag, filename) -> str:
    """Creates an ENTITY tag with proper name and path and appends it to the entity list."""
    entity = [tag, filename]
    return f'<!ENTITY {entity[0]} SYSTEM "./{entity[1]}">\n'


def save_file():
    """Saves the file to the user's desktop."""
    filepath = filedialog.asksaveasfilename(initialdir = "/",
        title="Save file", filetypes = (("xml files", "*.xml"),
        ("all files","*.*")))
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(textbox.get(1.0, END))
    filename = os.path.basename(filepath)
    messagebox.showinfo("File Saved", f'The file {filename} has been saved to {filepath}.')


root = ttk.Window("IADS PRODUCTION FILE GENERATOR", "darkly")
root.resizable(TRUE, FALSE)
root.geometry("1250x1500")

frame_top = ttk.Frame(root)
frame_top.pack(side=TOP, fill=X)

frame_btm = ttk.Frame(root)
frame_btm.pack(side=BOTTOM, fill=BOTH, expand=TRUE)

wip_btn = ttk.Button(frame_top, text="WIP FOLDER", command=open_wip_dir,
                     bootstyle="success")
wip_btn.pack(side=LEFT, fill=BOTH, expand=TRUE, padx=10, pady=(10, 0))

save_btn = ttk.Button(frame_top, text="SAVE FILE", bootstyle="success",
                      state="disabled", command=save_file)
save_btn.pack(side=RIGHT, fill=BOTH, expand=TRUE, padx=10, pady=(10, 0))

style = ttk.Style()
textbox = ScrolledText(
    master=frame_btm,
    font="Menlo",
    highlightcolor=style.colors.success,
    highlightbackground=style.colors.border,
    highlightthickness=1,
    wrap=WORD
)
textbox.pack(side=LEFT, fill=BOTH, expand=YES, padx=10, pady=10)

font = tkfont.Font(font=textbox['font'])
tab=font.measure("    ")
textbox.configure(tabs=tab)

root.mainloop()
