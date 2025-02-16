import PySimpleGUI as sg
import subprocess
import util
import os

menu_def = [['[F]ile', ['Extract',['NSP', '!XCI']]],['[M]isc', 'About']]

layout = [[sg.MenuBar(menu_def), sg.Output(size=(60, 5), background_color='Black',text_color='Green', font='None')]]

window = sg.Window('LazyExtractor [Alpha]').Layout(layout)

while True:
    event, value = window.Read()
    if event is None or event == 'Exit': #Case we click exit
        break
    if event == 'NSP':
        filename = sg.PopupGetFile('Open File', no_window=True, file_types=(("Switch File Types", "*.nsp"),))
        if filename != '':
            print ('Extracting NSP:')
            window.Refresh()
            print (subprocess.check_output(['squirrel', '-ogame_files/nca','--NSP_copy_nca', '%s' % filename]))
            window.Refresh()
            subprocess.check_output(['squirrel', '-ogame_files/nca', '--NSP_copy_ticket', '%s' % filename])
            subprocess.check_output(['squirrel', '-ogame_files/nca', '--NSP_copy_xml', '%s' % filename])
            window.Refresh()
            print ('Done!')
            window.Refresh()
            print ('Checking for Title Key File...')
            keyfile = util.find_tik()
            window.Refresh()
            print ('Grabbing title key for you...')
            window.Refresh()
            key = util.find_titlekey(keyfile)
            print ('title key found: %s' % key)
            window.Refresh()
            print ('Searching for Xml File...')
            if not util.xml_check():
                print ('No XML file found, Trying Biggest NCA File')
                print ('Finding Biggest NCA file...')
                window.Refresh()
                ncafile = util.find_biggest()[0]
                print ('Found Biggest NCA:: %s' % ncafile)
                print ('Extracting NCA file, Please wait.. May look like its doing nothing..')
                window.Refresh()
                print (subprocess.check_output(['hactool','-k keys.txt', '--titlekey=%s' % key, '-t', 'nca', '--romfsdir=game_files/romfs', '--exefsdir=game_files/exefs', 'game_files/nca/%s' % ncafile],stderr=subprocess.STDOUT))
                window.Refresh()
                print ('Thanks for waiting, check game_files directory.')
            else:
                print ('Parsing NSP XML file...')
                xmlnca = util.xml_check()
                print ('Extracting NCA file, PLEASE WAIT..May look like its doing nothing..')
                window.Refresh()
                print (subprocess.check_output(
                    ['hactool', '-k keys.txt', '--titlekey=%s' % key, '-t', 'nca', '--romfsdir=game_files/romfs',
                     '--exefsdir=game_files/exefs', 'game_files/nca/%s' % xmlnca], stderr=subprocess.STDOUT))
                window.Refresh()
                print ('Thanks for waiting, check game_files directory.')
    else:
        print ('')

    if event == 'XCI':
        filename = sg.PopupGetFile('Open File', no_window=True, file_types=(("Switch File Types", "*.xci"),))
        print (subprocess.check_output(['hactool', '-k keys.txt', '-t', 'xci', '--outdir=game_files', '%s' % filename] ))
        ncafile = util.find_biggest_xci()[0]
        print (subprocess.check_output(['hactool', '-k keys.txt', '-t', 'xci', '--romfsdir=game_files/romfs','--exefsdir=game_files/exefs', '%s' % ncafile]))

    if event == 'About':
        print ('LazyExtracter\n version: 0.3A\n Description: Allows the extraction of NSP and XCI Nintendo Switch files')




