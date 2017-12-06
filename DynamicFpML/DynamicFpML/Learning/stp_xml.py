import lxml.etree as ET
import os
# Will probably need to import all xml libs.

ELEM_TRACKER = 0
FAIL_COUNT = 0
SEP_XPATH = '/'
XPATH1 = SEP_XPATH
XPATH2 = SEP_XPATH
XPATH_SKIP_DICT = {}


class XMLError(Exception):
    """Represents an error code being returned from getting XML"""

    def __init__(self, criteria, result):
        self.criteria = criteria
        self.result = result


def GetXML(criteria):
    try:
        return eval(str(criteria)).toxml()
    except Exception as e:
        raise XMLError(str(criteria), str(e))


def buildXPathDict(xpath_exceptions=None):
    global XPATH_SKIP_DICT
    if xpath_exceptions == None:
        return
    if os.path.isfile(xpath_exceptions):
        with open(xpath_exceptions) as f:
            lines = f.readlines()
            for line in lines:
                for word in line.split():
                    XPATH_SKIP_DICT.setdefault(word, list()).append(line)


def indent_inplace(elem, level=0, whitespacestrip=True):
    ''' Alters the text nodes so that the tostring()ed version will look nicely indented.
 
        whitespacestrip can make contents that contain a lot of newlines look cleaner, 
        but changes the stored data even more.
    '''
    i = "\n" + level * "  "

    if whitespacestrip:
        if elem.text:
            elem.text = elem.text.strip()
        if elem.tail:
            elem.tail = elem.tail.strip()

    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent_inplace(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def prettyprint(xml, whitespacestrip=True):
    ''' Convenience wrapper around indent_inplace():
        - Takes a string (parses it) or a ET structure (in which case it changes it),
        - Reindents,
        - Returns the result as a string.
 
        whitespacestrip: see note in indent_inplace()
 
        Not horribly efficient, and alters the structure you gave it,
        but you are only using this for debug, right?
    '''
    if type(xml) is str:
        xml = ET.fromstring(xml)
    indent_inplace(xml, whitespacestrip)
    return ET.tostring(xml).rstrip('\n')


def compareText(t1, t2):
    if not t1 and not t2:
        return True
    if t1 == '*' or t2 == '*':
        return True
    return (t1 or '').strip() == (t2 or '').strip()


def traverseElements(elem1, elem2):
    global XPATH1, XPATH2, XPATH_SKIP_DICT, ELEM_TRACKER, FAIL_COUNT
    ELEM_TRACKER += 1
    XPATH1 = addTagToXPath(XPATH1, elem1)
    XPATH2 = addTagToXPath(XPATH2, elem2)
    doCompare = True
    if XPATH_SKIP_DICT.has_key(XPATH1): doCompare = False
    if XPATH_SKIP_DICT.has_key(XPATH2): doCompare = False
    children1 = elem1.getchildren()
    children2 = elem2.getchildren()
    if doCompare: compareElemInfo(elem1, elem2, children1, children2)
    for child1, child2 in zip(children1, children2):
        traverseElements(child1, child2)
    XPATH1 = delTagFromXPath(XPATH1)
    XPATH2 = delTagFromXPath(XPATH2)
    return


def addTagToXPath(xpath, elem):
    return xpath + SEP_XPATH + elem.xpath('local-name()')


def delTagFromXPath(xpath):
    tags = xpath.split(SEP_XPATH)
    del tags[-1]
    return SEP_XPATH.join(tags)


def diff(a, b):
    b = set(b)
    return [aa for aa in a if aa not in b]


def compareElemInfo(elem1, elem2, children1, children2):
    global ELEM_TRACKER, XPATH1, XPATH2, FAIL_COUNT

    if XPATH1 == '//FpML/tradeSTPHeader/docKey':
        print 'QATestTradeID: {}'.format(elem1.text)

    if not compareText(elem1.text, elem2.text):
        if XPATH1 == '//FpML/tradeSTPHeader/docKey':
            print 'QATestTradeID: {}'.format(elem1.text)
        FAIL_COUNT += 1
        print 'Difference %d: Element Text differs at %s. Expected: %s Actual: %s' % (
            FAIL_COUNT, XPATH1, elem1.text, elem2.text)

    for name, value in elem1.attrib.items():
        if elem2.attrib.get(name) and elem2.attrib.get(name) != value:
            FAIL_COUNT += 1
            print 'Difference %d: Attribute values at %s/@%s are different.  Expected: %s Actual: %s' % (
                FAIL_COUNT, XPATH1, name, value, elem2.attrib.get(name))

    if XPATH1 == XPATH2:
        c1 = [x.xpath('local-name()') for x in children1]
        c2 = [x.xpath('local-name()') for x in children2]
        a1 = elem1.attrib.keys()
        a2 = elem2.attrib.keys()
        missing = diff(c2, c1)
        new = diff(c1, c2)
        missing_attributes = diff(a2, a1)
        new_attributes = diff(a1, a2)
        if (new):
            new = list_diff('node', new)
            FAIL_COUNT += 1
            print 'Difference %d: Children at %s are different.  The %s new in the Actual Result.' % (
                FAIL_COUNT, XPATH1, new)
        if (missing):
            missing = list_diff('node', missing)
            FAIL_COUNT += 1
            print 'Difference %d: Children at %s are different.  The %s missing in the Actual Result.' % (
                FAIL_COUNT, XPATH1, missing)
        if (new_attributes):
            new_attributes = list_diff('attribute', new_attributes)
            FAIL_COUNT += 1
            print 'Difference %d: Attributes at %s are different.  The %s new in the Actual Result.' % (
                FAIL_COUNT, XPATH1, new_attributes)
        if (missing_attributes):
            missing_attributes = list_diff('attribute', missing_attributes)
            FAIL_COUNT += 1
            print 'Difference %d: Attributes at %s are different.  The %s missing in the Actual Result.' % (
                FAIL_COUNT, XPATH1, missing_attributes)
    return


def list_diff(singular, a):
    if len(a) == 1:
        return "%s %s is" % (singular, a[0])
    else:
        return "%ss %s are" % (singular, ', '.join(a))


def compareXML(xml1, xml2, xpath_exceptions=[]):
    try:
        global FAIL_COUNT, ELEM_TRACKER
        ELEM_TRACKER = 0
        buildXPathDict(xpath_exceptions)

        if xml1 == None:
            print 'No data supplied in xml1: %s' % (str(xml1))
            return -1
        if os.path.isfile(xml1):
            xml1Tree = ET.parse(xml1)
            xml1Root = xml1Tree.getroot()
        else:
            xml1Root = ET.fromstring(xml1)

        if xml2 == None:
            print 'No data supplied in xml2: %s' % (str(xml2))
            return -2
        if os.path.isfile(xml2):
            xml2Tree = ET.parse(xml2)
            xml2Root = xml2Tree.getroot()
        else:
            xml2Root = ET.fromstring(xml2)

        traverseElements(xml1Root, xml2Root)
        return FAIL_COUNT
    except Exception, e:
        print str(e)
        return -9
