from stp_log import RedirectOutput
import sys
import os

# import UI_Trial

pathReport = ''


class CompareXML:
    def __init__(self, path1, path2, logFile):
        self.path1 = path1
        self.path2 = path2
        self.logFile = logFile
        self.exceptionList = 'XPATH Exception file path'

        from stp_xml import compareXML
        # Make dir for log output
        logDir = os.path.dirname(self.logFile)
        if not os.path.exists(logDir):
            os.makedirs(logDir)
            # Redirect stdout to our log file.
            sys.stdout = open(self.logFile, 'w')
        else:
            sys.stdout = open(self.logFile, 'w')

        exitCode = compareXML(self.path1, self.path2, self.exceptionList)
        sys.stdout.close()

        with open(self.logFile, "a") as myfile:
            text_write = "Total_Compared: {0}\n\n".format(exitCode)
            myfile.write(text_write)
            # myfile.write("\n")
        #myfile.close()

        global pathReport
        # pathReport = genReport.createWorkbook(self.logFile)
        #return pathReport

    def path(cls):
        global pathReport
        return pathReport

    # def main(args):
    #     from stp_xml import compareXML
    #
    #     # Make dir for log output
    #     logDir = os.path.dirname(args.logFile)
    #     if not os.path.exists(logDir):
    #         os.makedirs(logDir)
    #     # Redirect stdout to our log file.
    #     sys.stdout = open(args.logFile, 'a')
    #
    #     exitCode = compareXML(args.xml1, args.xml2, args.exceptionList)
    #     sys.exit(exitCode)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--xml1', help='XML1 filepath')
    parser.add_argument('--xml2', help='XML2 filepath')
    parser.add_argument('--exceptionList', default=r'C:\Users\gaurav.saini\Desktop\DynamicFpML\DynamicFpML\DATA\exception_list.txt',
                        help='XPATH Exception file path')
    parser.add_argument('--logFile', default=r'C:\Users\gaurav.saini\Desktop\DynamicFpML\DynamicFpML\DATA\CompareXML.log',
                        help='full path of output log file')
    args = parser.parse_args()
    out = RedirectOutput(args.logFile, mode='w+')

    try:
        compXML = CompareXML(args.xml1, args.xml2, args.logFile)
    except Exception, e:
        print(e)
    finally:
        out.restore()
