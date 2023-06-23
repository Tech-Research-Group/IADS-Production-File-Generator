"""WORK PACKAGE CONVERTER"""
from tkinter import filedialog
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
    attributes = []
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
    _c = 1
    _o = 1
    _u = 1

    if filenames := filedialog.askopenfilenames():
        for path in filenames:
            filename = os.path.basename(path)
            
            # if "FrontMatter".lower() in filename.lower() or "Front_Matter".lower() in filename.lower() or "Front Matter".lower() in filename.lower() or "FrontCover".lower() in filename.lower() or "Front_Cover".lower() in filename.lower() or "Front Cover".lower() in filename.lower():
            #     with open(path, 'r', encoding='utf-8') as _f:
            #         for line in _f:
            #             line = line.lstrip("\t")
            #             if line.startswith("<tmno>"):
            #                 tmno = line[6:-8]
            #                 attributes.append(tmno)
            #                 maintlvls = re.findall(r"\d+$", tmno)
            #                 if maintlvls == [] or maintlvls == None:
            #                     maintlvls = re.findall(r"\d+\&amp;[pP]", tmno)
            #                     maintlvls = re.findall(r"\d+", maintlvls[0])
            #                 attributes.append(maintlvls[0])
            #             if line.startswith("<name>"):
            #                 name = line[6:-8]
            #                 attributes.append(name)
            #                 break
            #             if "RPSTL" in line or "Repair".lower() in filename.lower() and "Parts".lower() in filename.lower():
            #                 attributes.append("yes")
            #             else:
            #                 attributes.append("no")
            #         _f.close()
            if "Front".lower() in filename.lower() and "Cover".lower() in filename.lower():
                tag = "frntcover"
                paper_frnt_tag += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "Warning".lower() in filename.lower() or "Summary".lower() in filename.lower():
                tag = "warnsum"
                paper_frnt_tag += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "LOEP".lower() in filename.lower() or "Effective".lower() in filename.lower():
                tag = "loep"
                paper_frnt_tag += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "TitleBlock_TOC_HowToUse".lower() in filename.lower():
                tag = "tb_toc_htu"
                paper_frnt_tag += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            # elif "TitleBlock".lower() in filename.lower() or "Title_Block".lower() in filename.lower() or "TitleBlk".lower() in filename.lower():
            #     tag = "titleblk"
            #     paper_frnt_tag += f'&{tag}; '
            #     production_xml += f'\t{get_entity_data(tag, filename)}'
            # elif "TOC".lower() in filename.lower() or "TableOfContents".lower() in filename.lower() or "Table_Of_Contents".lower() in filename.lower():
            #     tag = "toc"
            #     paper_frnt_tag += f'&{tag}; '
            #     production_xml += f'\t{get_entity_data(tag, filename)}'
            # TODO Fix this TOC issue
            # else:
            #     production_xml += "\t\t\t<contents>\n\t\t\t\t<title/>\n\t\t\t\t<col.title/>\nt\t\t\t\t<col.title/>\n\t\t\t\t<contententry>\n\t\t\t\t\t<title/>\n\t\t\t\t</contententry>\n\t\t\t</contents>\n"
            elif "HowToUse".lower() in filename.lower() or "How_To_Use".lower() in filename.lower():
                tag = "howtouse"
                paper_frnt_tag += f'&{tag};\n\t'
                production_xml += f'\t{get_entity_data(tag, filename)}'
            # GENERAL INFORMATION, EQUIPMENT DESCRIPTION, and THEORY OF OPERATIONS
            elif "GenInfo".lower() in filename.lower() or "GeneralInfo".lower() in filename.lower() or "Gen_Info".lower() in filename.lower() or "General_Info".lower() in filename.lower() and "Chap".lower() not in filename.lower() and "START".lower() not in filename.lower():
                tag = "ginfowp"
                gim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "EqpDesc".lower() in filename.lower() or "Equipment Description".lower() in filename.lower() or "Equipment_Desc".lower() in filename.lower() or "General_Info".lower() in filename.lower():
                tag = "descwp"
                gim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "TheoryOps".lower() in filename.lower() or "TheoryOfOp".lower() in filename.lower() or "ThryOps".lower() in filename.lower() or "General_Info".lower() in filename.lower() or "ThryOps".lower() in filename.lower() or "Theory".lower() in filename.lower():
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
            elif "-O00" in filename and "unusual" not in filename.lower():
                if usual_entities == "":
                    tag = "opusualwp"
                    usual_entities += f'&{tag}; '
                else:
                    _o += 1
                    tag = f"opusualwp{_o}"
                    usual_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-O00" in filename and "unusual" in filename.lower():
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
            elif ("TS" in filename or "Troubleshooting" in filename) and "Intro" in filename:
                tag = "tsintrowp"
                new_tag = ""
                with open(path, "r", encoding="utf-8") as _f:
                    for line in _f:
                        line = line.lstrip("\t")
                        if line.startswith("<maintlvl level=") and "operator" in line:
                            new_tag = f'o{tag}'
                            tim_entities += f'&{new_tag}; '
                        elif line.startswith("<maintlvl level=") and "maintainer" in line:
                            new_tag = f'm{tag}'
                            mtim_entities += f'&{new_tag}; '
                        break
                    _f.close()
                production_xml += f'\t{get_entity_data(new_tag, filename)}'
            elif ("TS" in filename or "Troubleshooting" in filename) and "Index" in filename:
                tag = "tsindexwp"
                new_tag = ""
                with open(path, "r", encoding="utf-8") as _f:
                    for line in _f:
                        line = line.lstrip("\t")
                        if line.startswith("<maintlvl level=") and "operator" in line:
                            new_tag = f'o{tag}'
                            tim_entities += f'&{new_tag}; '
                        elif line.startswith("<maintlvl level=") and "maintainer" in line:
                            new_tag = f'm{tag}'
                            mtim_entities += f'&{new_tag}; '
                        break
                    _f.close()
                production_xml += f'\t{get_entity_data(new_tag, filename)}'
            elif "-T000" in filename and "intro" not in filename.lower() and "index" not in filename.lower() and "start" not in filename.lower() and "chap" not in filename.lower():
                tag = get_wp_code(filename)
                tim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-T001" in filename and "intro" not in filename.lower() and "index" not in filename.lower() and "start" not in filename.lower() and "chap" not in filename.lower():
                tag = get_wp_code(filename)
                mtim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'

            # PREVENTIVE MAINTENANCE CHECKS AND SERVICES (PMCS)
            elif "-M00" in filename and "PMCS" in filename and "Intro" in filename:
                tag = "pmcsintrowp"
                with open(path, "r", encoding="utf-8") as _f:
                    for line in _f:
                        line = line.lstrip("\t")
                        if line.startswith("<maintlvl level=") and "operator" in line:
                            mim_entities += f'&o{tag}; '
                        elif line.startswith("<maintlvl level=") and "maintainer" in line:
                            mim2_entities += f'&m{tag}; '
                        break
                    _f.close()
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-M00" in filename and "PMCS" in filename and "Daily".lower() in filename.lower() or "Weekly".lower() in filename.lower() or "Monthly".lower() in filename.lower() or "Quarterly".lower() in filename.lower() or "Semi-annually".lower() in filename.lower() or "Annually".lower() in filename.lower() or "Before".lower() in filename.lower() or "During".lower() in filename.lower() or "After".lower() in filename.lower():
                tag = get_wp_code(filename)
                with open(path, "r", encoding="utf-8") as _f:
                    for line in _f:
                        line = line.lstrip("\t")
                        if line.startswith("<maintlvl level=") and "operator" in line:
                            mim_entities += f'&{tag}; '
                        elif line.startswith("<maintlvl level=") and "maintainer" in line:
                            mim2_entities += f'&{tag}; '
                        break
                    _f.close()
                production_xml += f'\t{get_entity_data(tag, filename)}'
            
            # MAINTENANCE PROCEDURES
            elif "-M00" in filename and "PMCS" not in filename:
                tag = get_wp_code(filename)
                with open(path, "r", encoding="utf-8") as _f:
                    for line in _f:
                        line = line.lstrip("\t")
                        if line.startswith("<maintlvl level=") and "operator" in line:
                            omim_entities += f'&{tag}; '
                        elif line.startswith("<maintlvl level=") and "maintainer" in line:
                            mmim_entities += f'&{tag}; '
                        break
                    _f.close()
                production_xml += f'\t{get_entity_data(tag, filename)}'

            # DESTRUCTION OF EQUIPMENT TO PREVENT ENEMY USE
            elif "-D00" in filename and "Intro" in filename and "Destruct" in filename:
                tag = "destruct-introwp"
                dim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-D00" in filename and "Intro" not in filename.lower():
                tag = get_wp_code(filename)
                dim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'

            # REPAIR PARTS AND SPECIAL TOOLS LIST (RPSTL)
            elif "rpstl" in filename.lower() or "partsinfo" in filename.lower() and "intro" in filename.lower():
                tag = "introwp"
                pim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-R00" in filename and "intro" not in filename.lower() and "nsn" not in filename.lower() and "pn" not in filename.lower() and "bulk" not in filename.lower() and "partnumber" not in filename.lower() and "index" not in filename.lower():
                tag = get_wp_code(filename)
                pim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-R00" in filename and "Bulk" in filename and "Item" in filename:
                tag = "bulk_itemswp"
                pim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-R00" in filename and "NSN" in filename and "Index" in filename:
                tag = "nsnindxwp"
                pim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-R00" in filename and "PN" in filename or "Part" in filename and "Index" in filename:
                tag = "pnindxwp"
                pim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'

            # SUPPORTING INFORMATION
            elif "-S00" in filename and "Reference" in filename:
                tag = "refwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-S00" in filename and "macintro" in filename.lower() or "mac_intro" in filename.lower() or "mac`" in filename.lower():
                tag = "macintrowp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-S00" in filename and "MAC" in filename:
                tag = "macwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-S00" in filename and "COEI" in filename or "BII" in filename :
                tag = "coeibiiwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-S00" in filename and "Expendable" in filename or "Durable" in filename or "EDIL" in filename:
                tag = "explistwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-S00" in filename and "AAL" in filename or "Additional" in filename and "Authorization" in filename:
                tag = "aalwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-S00" in filename and "TIL" in filename or "Tool" in filename and "Identification" in filename:
                tag = "tilwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-S00" in filename and "MRP" in filename or "Mandatory" in filename and "Replacement" in filename:
                tag = "mrplwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-S00" in filename and "CSI" in filename or "Critical" in filename and "Safety" in filename:
                tag = "csi.wp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-S00" in filename and "support" in filename.lower() and "item" in filename.lower():
                tag = "supitemwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            elif "-S00" in filename and "additional" in filename.lower() and "supporting" in filename.lower():
                tag = "genwp"
                sim_entities += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
            
            # REAR MATTER
            elif "rear" in filename.lower() and "matter" in filename.lower():
                tag = "rear"
                rear_entity += f'&{tag}; '
                production_xml += f'\t{get_entity_data(tag, filename)}'
                break

    # Concatenate XML file by tags/sections
    # paper_manual_tag = f'<paper.manual maintitl="{attributes[2]}" maintlvls="{attributes[1]}" revno="0" rpstl="{attributes[3]}" pubno="{attributes[0]}">'
    paper_manual_tag = '<paper.manual maintitl="" maintlvls="" revno="0" rpstl="" pubno="">'
    production_xml += f'{DOCTYPE_CLOSE}\n{production_tag}\n\t{paper_manual_tag}\n\t\t{paper_frnt_tag}\n\t\t</paper.frnt>\n'
    production_xml += '\t\t<gim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>General Information</name>\n\t\t\t</titlepg>\n'
    production_xml += f'\t\t\t{gim_entities}\n\t\t</gim>\n'
    if opim_entities != '':
        production_xml += '\t\t<opim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>Operator Instructions</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t{opim_entities}{usual_entities}{unusual_entities}\n\t\t</opim>\n'
    if tsim_entities != '':
        production_xml += '\t\t<tim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>Troubleshooting Master Index</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t{tsim_entities}\n\t\t</tim>\n'
    if tim_entities != '':
        production_xml += '\t\t<tim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>Operator Troubleshooting</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t{tim_entities}\n\t\t</tim>\n'
    if mtim_entities != '':
        production_xml += '\t\t<tim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>Maintainer Troubleshooting</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t{mtim_entities}\n\t\t</tim>\n'
    if mim_entities != '':
        production_xml += '\t\t<mim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>Operator PMCS</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t{mim_entities}\n\t\t</mim>\n'
    if mim2_entities != '':
        production_xml += '\t\t<mim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>Maintainer PMCS</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t{mim2_entities}\n\t\t</mim>\n'
    if omim_entities != '':
        production_xml += '\t\t<mim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>Operator Maintenance</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t{omim_entities}\n\t\t</mim>\n'
    if mmim_entities != '':
        production_xml += '\t\t<mim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>Maintainer Maintenance</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t{mmim_entities}\n\t\t</mim>\n'
    if dim_entities != '':
        production_xml += '\t\t<dim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>Destruction of Equipment</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t{dim_entities}\n\t\t</dim>\n'
    if pim_entities != '':
        production_xml += '\t\t<pim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>Repair Parts and Special Tools List</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t{pim_entities}\n\t\t</pim>\n'
    if sim_entities != '':
        production_xml += '\t\t<sim revno="0" chngno="0">\n\t\t\t<titlepg maintlvl="operator">\n\t\t\t\t<name>Supporting Information</name>\n\t\t\t</titlepg>\n'
        production_xml += f'\t\t\t{sim_entities}\n\t\t</sim>\n'
    
    if rear_entity != '':
        production_xml += f'\t\t{rear_entity}\n'
    production_xml += '\t</paper.manual>\n</production>'
    textbox.insert(END, production_xml)
    textbox.configure(state="normal")
    textbox.update()


def get_entity_data(tag, filename) -> str:
    """Creates an ENTITY tag with proper name and path and appends it to the entity list."""
    path = filename
    entity = [tag, path]
    return f'<!ENTITY {entity[0]} SYSTEM "./{entity[1]}">\n'


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
                      state="disabled")
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
