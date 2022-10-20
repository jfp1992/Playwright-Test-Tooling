class Xpath:
    """Allows quick templating of basic Xpaths or the start of longer ones
    example: //tag[@attribute='attribute value']
    :param tag: Examples: div, a, li, ul, Span, OtherAnything
    :param att: Examples: class@, class(), text(), @anything
    :param val: Value of attribute (after the =)
    :return: f"//{tag}[{attribute}='{value}']" """

    def __init__(self, tag=None, att=None, val=None, rel=None, index=None):
        if not tag and not att and not val:
            raise ValueError("No arguments passed for tag, attribute and value")
        if att[0] != "@" and att != "text":
            att = "@" + att
        else:
            att = att + "()"

        self.tag = tag
        self.att = att
        self.val = val
        self.rel = rel
        if index is not None:
            self.index = str(index)
        else:
            self.index = index

    def xpath_type_logic(self, xstart, xchain):
        if self.index is None:
            if self.rel is None:
                return xstart
            else:
                return xchain
        else:
            if self.rel is None:
                return f"{xstart}[{self.index}]"
            else:
                return f"{xchain}[{self.index}]"

    def absolute(self):
        xstart = f"//{self.tag}[{self.att}='{self.val}']"
        xchain = f"/{self.rel}::{self.tag}[{self.att}='{self.val}']"
        return self.xpath_type_logic(xstart, xchain)

    def starts_with(self):
        xstart = f"//{self.tag}[starts-with({self.att}, '{self.val}')]"
        xchain = f"/{self.rel}::{self.tag}[starts-with({self.att}, '{self.val}')]"
        return self.xpath_type_logic(xstart, xchain)

    def ends_with(self):
        xstart = f"//{self.tag}['{self.val}' = substring({self.att}, string-length({self.att}) - string-length('{self.val}') +1)]"
        xchain = (
            f"/{self.rel}::{self.tag}['{self.val}' = substring({self.att}, string-length({self.att}) - string-length('{self.val}') +1)]"
        )
        return self.xpath_type_logic(xstart, xchain)

    def contains(self):
        xstart = f"//{self.tag}[contains({self.att}, '{self.val}')]"
        xchain = f"/{self.rel}::{self.tag}[contains({self.att}, '{self.val}')]"
        return self.xpath_type_logic(xstart, xchain)


class Css:
    """Allows quick templating of basic css selectors
    example: tag[attribute='attribute value']
    :param tag: Examples: div, a, li, ul, Span, OtherAnything
    :param att: Examples: class@, class(), @anything
    :param val: Value of attribute (after the =)
    :return: f"{tag}[{attribute}='{value}']" """

    def __init__(self, tag=None, att=None, val=None, rel=None):
        if not tag and not att and not val:
            raise ValueError("No arguments passed for tag, attribute and value")

        self.tag = tag
        self.att = att
        self.val = val
        self.rel = rel

    def build_css(self, value_modifier):
        if self.rel == "child" or self.rel == ">":
            combinator = f" > "
        elif self.rel == "descendant" or self.rel == " ":
            combinator = " "
        else:
            combinator = ""

        css = f"{combinator}{self.tag}[{self.att}{value_modifier}='{self.val}']"
        return css

    def absolute(self):
        return self.build_css("")

    def contains(self):
        return self.build_css("*")

    def starts_with(self):
        return self.build_css("^")

    def ends_with(self):
        return self.build_css("$")
