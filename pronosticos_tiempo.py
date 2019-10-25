# -*- coding: UTF-8 -*-

#import system modules
import arcpy
from arcpy import env
import os
#import xml.dom.minidom as DOM 

#set env
project_folder = r'D:\herramientas\pronosticos_lluvia'
env.workspace = project_folder
arcpy.env.overwriteOutput = True

#date
date = datetime.datetime.today().strftime('%Y%m%d')

#default paths
gfs_today = project_folder + r'\gfs_precip_shp_tif_' + date
gfs_24h = gfs_today + r'\gfs_precip_gis_24_' + date + r'.shp'
gfs_48h = gfs_today + r'\gfs_precip_gis_48_' + date + r'.shp'
gfs_72h = gfs_today + r'\gfs_precip_gis_72_' + date + r'.shp'
gfs_96h = gfs_today + r'\gfs_precip_gis_96_' + date + r'.shp'
gfs_120h = gfs_today + r'\gfs_precip_gis_120_' + date + r'.shp'
gfs_144h = gfs_today + r'\gfs_precip_gis_144_' + date + r'.shp'
gfs_168h = gfs_today + r'\gfs_precip_gis_168_' + date + r'.shp'
gfs_7day = gfs_today + r'\gfs_precip_gis_7day_' + date + r'.shp'
costa_rica = project_folder + r'\pronosticos\default.gdb\area_cafe'
project_gdb = project_folder + r'\pronosticos\default.gdb'


#outputs
gfs_24h_cr = project_gdb + r'\gfs_24h_cr'
gfs_48h_cr = project_gdb + r'\gfs_48h_cr'
gfs_72h_cr = project_gdb + r'\gfs_72h_cr'
gfs_96h_cr = project_gdb + r'\gfs_96h_cr'
gfs_120h_cr = project_gdb + r'\gfs_120h_cr'
gfs_144h_cr = project_gdb + r'\gfs_144h_cr'
gfs_168h_cr = project_gdb + r'\gfs_168h_cr'
gfs_7day_cr = project_gdb + r'\gfs_7day_cr'



#function for delete overlap into layers and create dates fields
def delete_overlap(layer):
    arcpy.analysis.Union(layer, layer + r'_union', "ALL", None, "GAPS")
    arcpy.AddField_management(layer + r'_union', 'x_coord', 'DOUBLE')
    arcpy.AddField_management(layer + r'_union', 'y_coord', 'DOUBLE')
    arcpy.AddField_management(layer + r'_union', 'xy', 'text')
    arcpy.management.CalculateGeometryAttributes(layer + r'_union', "x_coord CENTROID_X;y_coord INSIDE_Y", '', '', None)
    arcpy.management.CalculateField(layer + r"_union", "xy", 'str(!x_coord!) + " " + str(!y_coord!)', "PYTHON3", '')
    arcpy.analysis.Statistics(layer + r'_union', layer + r'_maxvalue', "Contour MAX", "xy")
    join = arcpy.management.AddJoin(layer + r'_union', "xy", layer + r'_maxvalue', "xy", "KEEP_ALL")
    arcpy.CopyFeatures_management(join, layer + r'_max')
    arcpy.management.Dissolve(layer + r'_max', layer, layer[59:] + '_maxvalue_' + 'MAX_Contour', None, "SINGLE_PART", "DISSOLVE_LINES")
    #create_time_fields
    arcpy.AddField_management(layer,'inicio', 'DATE')
    arcpy.AddField_management(layer,'final', 'DATE')
    #Calculate start and end dates
    arcpy.AddField_management(layer, 'Contour', 'DOUBLE')
    arcpy.CalculateField_management(layer, 'Contour', '!' + layer[59:] + '_maxvalue_' + 'MAX_Contour' + '!', "PYTHON3", '')
    arcpy.DeleteField_management(layer, layer[59:] + '_maxvalue_' + 'MAX_Contour')
    

#24 hours
print('working 24h')
arcpy.Clip_analysis(gfs_24h,costa_rica,gfs_24h_cr)
delete_overlap(gfs_24h_cr)
#calculate start and end dates
arcpy.CalculateField_management(gfs_24h_cr, 'inicio','datetime.datetime.now().replace(hour=0, minute=0, second=0)')
arcpy.CalculateField_management(gfs_24h_cr, 'final','datetime.datetime.now().replace(hour=23, minute=59, second=59)')
print("24h ready")

#48 hours
print('working 48h')
arcpy.Clip_analysis(gfs_48h,costa_rica,gfs_48h_cr)
delete_overlap(gfs_48h_cr)
#Calculate start and end dates
arcpy.CalculateField_management(gfs_48h_cr, 'inicio','datetime.datetime.now().replace(hour=0, minute=0, second=0) + datetime.timedelta(days=1)', 'PYTHON3')
arcpy.CalculateField_management(gfs_48h_cr, 'final','datetime.datetime.now().replace(hour=23, minute=59, second=59) + datetime.timedelta(days=1)', 'PYTHON3')
print("48h ready")

#clip 72 hours
print('working 72h')
arcpy.Clip_analysis(gfs_72h,costa_rica,gfs_72h_cr)
delete_overlap(gfs_72h_cr)
#Calculate start and end dates
arcpy.CalculateField_management(gfs_72h_cr, 'inicio','datetime.datetime.now().replace(hour=0, minute=0, second=0) + datetime.timedelta(days=2)', 'PYTHON3')
arcpy.CalculateField_management(gfs_72h_cr, 'final','datetime.datetime.now().replace(hour=23, minute=59, second=59) + datetime.timedelta(days=2)', 'PYTHON3')
print("48h ready")

#clip 96 hours
print('working 96h')
arcpy.Clip_analysis(gfs_96h,costa_rica,gfs_96h_cr)
delete_overlap(gfs_96h_cr)
#Calculate start and end dates
arcpy.CalculateField_management(gfs_96h_cr, 'inicio','datetime.datetime.now().replace(hour=0, minute=0, second=0) + datetime.timedelta(days=3)', 'PYTHON3')
arcpy.CalculateField_management(gfs_96h_cr, 'final','datetime.datetime.now().replace(hour=23, minute=59, second=59) + datetime.timedelta(days=3)', 'PYTHON3')
print("96h ready")

#clip 120 hours
print('working 120h')
arcpy.Clip_analysis(gfs_120h,costa_rica,gfs_120h_cr)
delete_overlap(gfs_120h_cr)
#Calculate start and end dates
arcpy.CalculateField_management(gfs_120h_cr, 'inicio','datetime.datetime.now().replace(hour=0, minute=0, second=0) + datetime.timedelta(days=4)', 'PYTHON3')
arcpy.CalculateField_management(gfs_120h_cr, 'final','datetime.datetime.now().replace(hour=23, minute=59, second=59) + datetime.timedelta(days=4)', 'PYTHON3')
print("120h ready")

#clip 144 hours
print('working 144h')
arcpy.Clip_analysis(gfs_144h,costa_rica,gfs_144h_cr)
delete_overlap(gfs_144h_cr)
#Calculate start and end dates
arcpy.CalculateField_management(gfs_144h_cr, 'inicio','datetime.datetime.now().replace(hour=0, minute=0, second=0) + datetime.timedelta(days=5)', 'PYTHON3')
arcpy.CalculateField_management(gfs_144h_cr, 'final','datetime.datetime.now().replace(hour=23, minute=59, second=59) + datetime.timedelta(days=5)', 'PYTHON3')
print("144h ready")

#clip 168 hours
print('working 168h')
arcpy.Clip_analysis(gfs_168h,costa_rica,gfs_168h_cr)
delete_overlap(gfs_168h_cr)
#Calculate start and end dates
arcpy.CalculateField_management(gfs_168h_cr, 'inicio','datetime.datetime.now().replace(hour=0, minute=0, second=0) + datetime.timedelta(days=6)', 'PYTHON3')
arcpy.CalculateField_management(gfs_168h_cr, 'final','datetime.datetime.now().replace(hour=23, minute=59, second=59) + datetime.timedelta(days=6)', 'PYTHON3')
print("168h ready")

#clip 7 days
#arcpy.Clip_analysis(gfs_7day,costa_rica,gfs_7day_cr)
#create_time_fields
#arcpy.AddField_management(gfs_7day_cr,'inicio', 'DATE')
#arcpy.AddField_management(gfs_7day_cr,'final', 'DATE')
#Calculate start and end dates
#arcpy.CalculateField_management(gfs_7day_cr, 'inicio','datetime.datetime.now().replace(hour=0, minute=0, second=0)', 'PYTHON3')
#arcpy.CalculateField_management(gfs_7day_cr, 'final','datetime.datetime.now().replace(hour=23, minute=59, second=59)', 'PYTHON3')

#Merge of all cliped layers
print('Mergging all layers')
arcpy.Merge_management([gfs_24h_cr, gfs_48h_cr, gfs_72h_cr, gfs_96h_cr, gfs_120h_cr, gfs_144h_cr, gfs_168h_cr], project_gdb + r'\precipitacion', r'Contour "Contour" true true false 4 Long 0 0,First,#,gfs_168h_cr,Contour,-1,-1,gfs_120h_cr,Contour,-1,-1,gfs_144h_cr,Contour,-1,-1,gfs_24h_cr,Contour,-1,-1,gfs_48h_cr,Contour,-1,-1,gfs_72h_cr,Contour,-1,-1,gfs_96h_cr,Contour,-1,-1;inicio "inicio" true true false 8 Date 0 0,First,#,gfs_168h_cr,inicio,-1,-1,gfs_120h_cr,inicio,-1,-1,gfs_144h_cr,inicio,-1,-1,gfs_24h_cr,inicio,-1,-1,gfs_48h_cr,inicio,-1,-1,gfs_72h_cr,inicio,-1,-1,gfs_96h_cr,inicio,-1,-1;final "final" true true false 8 Date 0 0,First,#,gfs_168h_cr,final,-1,-1,gfs_120h_cr,final,-1,-1,gfs_144h_cr,final,-1,-1,gfs_24h_cr,final,-1,-1,gfs_48h_cr,final,-1,-1,gfs_72h_cr,final,-1,-1,gfs_96h_cr,final,-1,-1', "NO_SOURCE_INFO")
print('layers merged')

#create label field
arcpy.AddField_management(project_gdb + r'\precipitacion', 'label', 'text')
arcpy.management.CalculateField(project_gdb + r'\precipitacion', "label", "stringday(!inicio!, !Contour!)", "PYTHON3", "def stringday(inicio, mm):\n    weekDays = (\"Lunes\",\"Martes\",\"Miercoles\",\"Jueves\"," +
    "\"Viernes\",\"Sabado\",\"Domingo\")\n    day = inicio.weekday()\n    daystring = weekDay" +
    "s[day]\n    label = \'El \' + daystring + \' lloverá \' + str(mm) + \'mm en esta región\'\n    return(l" +
    "abel)")


#import arcgis project aprx
aprx = arcpy.mp.ArcGISProject(project_folder + r'\pronosticos\pronosticos.aprx')


#save project
print('saving project')
aprx.save()
print('project saved')

#connect to arcgis portal
arcpy.SignInToPortal("https://sig.icafe.cr/portal","adminicafe","icafesig")

#Create sddraft
print("Creating sddraft")
m =  aprx.listMaps('Map')[0]
service = "pronosticos_image"
sddraft_filename = service + ".sddraft"
sddraft_output_filename = os.path.join(project_folder, sddraft_filename)

sharing_draft = m.getWebLayerSharingDraft("FEDERATED_SERVER", "MAP_IMAGE", service)
sharing_draft.federatedServerUrl = 'https://sig.icafe.cr/server'
sharing_draft.summary = "Pronosticos de precipitación"
sharing_draft.tags = "Pronosticos Precipitación"
sharing_draft.overwriteExistingService = True
sharing_draft.portalFolder = 'Pronosticos'

sharing_draft.exportToSDDraft(sddraft_output_filename)
print("sddraft created")

# Execute StageService
print("Creating sd file")
sd_filename = service + ".sd"
sd_output_filename = os.path.join(project_folder, sd_filename)
arcpy.StageService_server(sddraft_output_filename, sd_output_filename)
print("SD file created")

# Execute UploadServiceDefinition
print("Uploading...")
arcpy.UploadServiceDefinition_server(sd_output_filename, 'https://sig.icafe.cr/server')
print("Service uploaded")
print("""___________________▄▄▄▀▀▀▀▀▀▀▄
 _______________▄▀▀____▀▀▀▀▄____█
 ___________▄▀▀__▀▀▀▀▀▀▄___▀▄___█
 __________█▄▄▄▄▄▄_______▀▄__▀▄__█
 _________█_________▀▄______█____█_█
 ______▄█_____________▀▄_____▐___▐_▌
 ______██_______________▀▄___▐_▄▀▀▀▄
 ______█________██_______▌__▐▄▀______█
 ______█_________█_______▌__▐▐________▐
 _____▐__________▌_____▄▀▀▀__▌_______▐_____________▄▄▄▄▄▄
 ______▌__________▀▀▀▀________▀▀▄▄▄▀______▄▄████▓▓▓▓▓▓▓███▄
 ______▌____________________________▄▀__▄▄█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▄
 ______▐__________________________▄▀_▄█▓▓▓▓▓▓▓▓▓▓_____▓▓____▓▓█▄
 _______▌______________________▄▀_▄█▓▓▓▓▓▓▓▓▓▓▓____▓▓_▓▓_▓▓__▓▓█
 _____▄▀▄_________________▄▀▀▌██▓▓▓▓▓▓▓▓▓▓▓▓▓__▓▓▓___▓▓_▓▓__▓▓█
 ____▌____▀▀▀▄▄▄▄▄▄▄▄▀▀___▌█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓__▓________▓▓___▓▓▓█
 _____▀▄_________________▄▀▀▓▓▓▓▓▓▓▓█████████████▄▄_____▓▓__▓▓▓█
 _______█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓▓▓▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▄▄___▓▓▓▓▓█
 _______█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓▓███▓▓▓▓████▓▓▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓▓█
 ________█▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓█▓▓██░░███████░██▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓█
 ________█▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓░░░░░█░░░░░██░░░░██▓▓▓▓▓▓▓▓▓██▓▓▓▓▌
 ________█▓▓▓▓▓▓▓▓▓▓▓▓▓▓███░░░░░░░░____░██░░░░░░░██▓▓▓▓▓▓▓██▓▓▌
 ________▐▓▓▓▓▓▓▓▓▓▓▓▓▓▓██░░░░░░░________░░░░░░░░░██████▓▓▓▓▓█▓▌
 ________▐▓▓▓▓▓▓▓▓▓▓▓▓▓▓██░░░░░░___▓▓▓▓▓░░░░░░░███░░███▓▓▓▓▓█▓▌
 _________█▓▓▓▓▓▓▓▓▓▓▓▓▓██░░░░░___▓▓█▄▄▓░░░░░░░░___░░░░█▓▓▓▓▓█▓▌
 _________█▓▓▓▓▓▓▓▓▓▓▓▓▓█░░█░░░___▓▓██░░░░░░░░▓▓▓▓__░░░░█▓▓▓▓██
 _________█▓▓▓▓▓▓▓▓▓▓▓▓▓█░███░░____▓░░░░░░░░░░░█▄█▓__░░░░█▓▓█▓█
 _________▐▓▓▓▓▓▓▓▓▓▓▓▓▓█░█████░░░░░░░░░░░░░░░░░█▓__░░░░███▓█
 __________█▓▓▓▓▓▓▓▓▓▓▓▓█░░███████░░░░░░░░░░░░░░░▓_░░░░░██▓█
 __________█▓▓▓▓▓▓▓▓▓▓▓▓█░░░███████░░░░░░░░░░░░░░_░░░░░██▓█
 __________█▓▓▓▓▓▓▓▓▓▓▓▓█░░░███████░░░░░░░░░░░░░░░░░░░██▓█
 ___________█▓▓▓▓▓▓▓▓▓▓▓▓█░░░░███████░░░░░░░░░░░█████░██░░░
 ___________█▓▓▓▓▓▓▓▓▓▓▓▓█░░░░░░__███████░░░░░███████░░█░░░░
 ___________█▓▓▓▓▓▓▓▓▓▓▓▓▓█░░░░░░█▄▄▄▀▀▀▀████████████░░█░░░░
 ___________▐▓▓▓▓▓▓▓▓▓▓▓▓█░░░░░░██████▄__▀▀░░░███░░░░░█░░░
 ___________▐▓▓▓▓▓▓▓▓▓▓▓█▒█░░░░░░▓▓▓▓▓███▄░░░░░░░░░░░░░░░______▄▄▄
 ___________█▓▓▓▓▓▓▓▓▓█▒▒▒▒█░░░░░░▓▓▓▓▓█░░░░░░░░░░░░░░░▄▄▄_▄▀▀____▀▄
 __________█▓▓▓▓▓▓▓▓▓█▒▒▒▒█▓▓░░░░░░░░░░░░░░░░░░░░░____▄▀____▀▄_________▀▄
 _________█▓▓▓▓▓▓▓▓▓█▒▒▒▒█▓▓▓▓░░░░░░░░░░░░░░░░░______▐▄________█▄▄▀▀▀▄__█
 ________█▓▓▓▓▓▓▓▓█▒▒▒▒▒▒█▓▓▓▓▓▓▓░░░░░░░░░____________█_█______▐_________▀▄▌
 _______█▓▓▓▓▓▓▓▓█▒▒▒▒▒▒███▓▓▓▓▓▓▓▓▓▓▓█▒▒▄___________█__▀▄____█____▄▄▄____▐
 ______█▓▓▓▓▓▓▓█_______▒▒█▒▒██▓▓▓▓▓▓▓▓▓▓█▒▒▒▄_________█____▀▀█▀▄▀▀▀___▀▀▄▄▐
 _____█▓▓▓▓▓██▒_________▒█▒▒▒▒▒███▓▓▓▓▓▓█▒▒▒██________▐_______▀█_____________█
 ____█▓▓████▒█▒_________▒█▒▒▒▒▒▒▒▒███████▒▒▒▒██_______█_______▐______▄▄▄_____█
 __█▒██▒▒▒▒▒▒█▒▒____▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒____▒█▓█__▄█__█______▀▄▄▀▀____▀▀▄▄█
 __█▒▒▒▒▒▒▒▒▒▒█▒▒▒████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█_______█▓▓█▓▓▌_▐________▐____________▐
 __█▒▒▒▒▒▒▒▒▒▒▒███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒_______█▓▓▓█▓▌__▌_______▐_____▄▄____▐
 _█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒_____█▓▓▓█▓▓▌__▌_______▀▄▄▀______▐
 _█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███████▓▓█▓▓▓▌__▀▄_______________▄▀
 _█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███▒▒▒▒▒▒▒██▓▓▓▓▓▌___▀▄_________▄▀▀
 █▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒█▓▓▓▓▓▀▄__▀▄▄█▀▀▀
 █▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▓▓▓▓██▄▄▄▀
 █▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒████
 █▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
 _█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▄▄▄▄▄
 _█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███▒▒▒▒▒▒██▄▄
 __█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒███▒▒▒▒▒▒▒▒▒▒▒▒▒█▄
 __█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
 __█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒█▒▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
 ___█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒█▒▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▒▒▒▒▌
 ____█▒▒▒▒▒▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒█▒▒▒▒█▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░▒▒▌
 ____█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█████████████▒▒▒▒▒█▒▒▒▒▒▒▒▒░░░░▒▒▒▒▒▒▒▒▒▒▒░▒▌
 _____█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█_______▐▒▒▒▒█▒▒▒▒▒▒▒░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▌
 ______█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█________█▒▒█▒▒▒▒▒▒░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌
 _______█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█________█▒█▒▒▒▒▒▒░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌
 ________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█________█▒▒▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
 _________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█________█▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
 _________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█________█▒▒▒░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▀
 __________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█_______█▒░░░▒▒▒▒▒░░░░░░░░▒▒▒█▀▀▀
 ___________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█_______█░▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░█▀
 ____________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█_______█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▀
 _____________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█_______█▒▒▒▒▒▒▒▒▒▒▒▒█▀
 _____________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█_______▀▀▀███████▀▀
 ______________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
 _______________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
 ________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
 _________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
 __________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▒█
 ___________________█▒▒▒▒▒▒▒▒▒▒▒▒▒██▒▒▒▒█
 ___________________█▒▒▒▒▒▒▒▒████▒▒▒▒▒▒▒█
 ___________________█████████▒▒▒▒▒▒▒▒▒▒▒█
 ____________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
 ____________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
 _____________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▌
 _____________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▌
 ______________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▌
 _______________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░█
 ________________________█▒▒▒▒▒▒▒▒▒▒▒░░░█
 __________________________██▒▒▒▒▒▒░░░█▀
 _____________________________█░░░░░█▀
 _______________________________▀▀▀▀""")