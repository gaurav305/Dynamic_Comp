from stp_log import RedirectOutput
import sys, os, genReport


def main(args):
    from stp_xml import compareXML

    # Make dir for log output
    logDir = os.path.dirname(args.logFile)
    if not os.path.exists(logDir):
        os.makedirs(logDir)
    # Redirect stdout to our log file.
    sys.stdout = open(args.logFile, 'a')

    exitCode = compareXML(args.xml1, args.xml2, args.exceptionList)
    sys.stdout.close()
    genReport.createWorkbook(args.logFile)
    sys.exit(exitCode)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--xml1', help='XML1 filepath')
    parser.add_argument('--xml2', help='XML2 filepath')
    parser.add_argument('--exceptionList', help='XPATH Exception file path')
    parser.add_argument('--logFile', default=r'D:\MarkitServ\BAU\Python\xml_compare\xml-test\Learning\CompareXML.log',
                        help='full path of output log file')
    args = parser.parse_args()
    out = RedirectOutput(args.logFile, mode='w+')

    try:
        main(args)
    except Exception, e:
        print(e)
    finally:
        out.restore()
