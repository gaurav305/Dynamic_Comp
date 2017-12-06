from xlrd import open_workbook
import compare_XML
import genReport

class FetchData:
    def __init__(self,filepath):
        book = open_workbook(filepath)
        sheet = book.sheet_by_index(0)
        # read values into the list
        self.logFile = r'D:\MarkitServ\BAU\Python\DynamicFpML\DATA\CompareXML.log'

        list_of_list = []
        for row_index in xrange(sheet.nrows):
            list_row = []
            for col_index in xrange(sheet.ncols):
                l = sheet.cell(row_index, col_index).value
                list_row.append(l)
            list_of_list.append(list_row)

        print list_of_list

        for f in list_of_list:
            """for f1 in f:
                print f1"""
            #self._compare(f[0],f[1])
            compare_XML.CompareXML(f[0], f[1], self.logFile)

        # genReport.createWorkbook(self.logFile)

    def _compare(self,file1,file2):
        print "Files to be compared are %s and %s ."%(str(file1),str(file2))



if __name__ == '__main__':
    data_to_compare = FetchData(r'D:\MarkitServ\BAU\Python\DynamicFpML\ListOfFilesToBeCompared.xlsx')