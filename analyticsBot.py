# Import the libraries
import os
import pandas as pd


class analyticsBot(object):
    def myVariables(self):
        sql_dict = {"select": ['which', 'what', 'show', 'tell', "give"],
                    "where": [""]}

        sql_col_dict = {"employee_salary": ["salary", "salaries"],
                        "employee_id": ["id", "ids"],
                        "employee_name": ["name", "names"]}

        num_cols = ["employee_salary", "employee_id"]

        sql_compare_dict = {">": ["above", "greater"],
                            "<": ["below", "less"]}

        sql_agg_dict = {"max": ["max", "maximum", "highest"],
                        "min": ["min", 'minimum', "lowest"],
                        "avg": ["avg", "average", "mean"],
                        "sum": ['total', 'sum']
                        }

        sql_val_dict = {
            "employee_salary": ["50880", "80000", "60000", "110000", "135000", "23500", "12900", "35890", "52880",
                                "92580", "53060", "76980", "8890", "12580", "98990"],
            "employee_id": ["1", '2', "3", "4", "5", "6", '7', "8", "9", "10"],
            "employee_name": ["gazal", "abhishek", "santhosh", "sowmya", 'paritosh', "chris", "tom", "kevin", "stark",
                              "irfan"]}

        return sql_dict, sql_col_dict, num_cols, sql_compare_dict, sql_agg_dict, sql_val_dict

    def getCompareColumn(self,findlist, sql_col_dict, num_cols):
        for j in reversed(findlist):
            for sid, sval in sql_col_dict.items():
                if (j in sval and sid in num_cols):
                    return sid
        return None

    def getCompareVal(self,findlist):
        for j in findlist:
            if (j.isdigit()):
                return j
        return None

    def getAggColumn(self,findlist, sql_col_dict, num_cols):
        for j in findlist:
            for sid, sval in sql_col_dict.items():
                if (j in sval and sid in num_cols):
                    return sid
        return None

    def generateQuery(self,query):
        sql_dict, sql_col_dict, num_cols, sql_compare_dict, sql_agg_dict, sql_val_dict = self.myVariables()
        myquery = ["select"]
        querywords = query.split(" ")
        aggcols = []

        selectcols = []
        wherecols = []
        for i, q in enumerate(querywords):
            # print(q,aggcols)
            # for sid, sval in sql_dict.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
            #    if q in sval:
            #        if sid not in aggcols:
            #            myquery.append(sid)

            for sid, sval in sql_col_dict.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                if q in sval:
                    if sid not in aggcols:
                        # myquery.append(sid)
                        selectcols.append(sid)

            for sid, sval in sql_val_dict.items():
                if q in sval:
                    wherecols.append(sid + " like '" + q + "'")

            compare_col = None
            compare_val = None
            for cid, cval in sql_compare_dict.items():
                if q in cval:
                    compare_col = self.getCompareColumn(querywords[:i], sql_col_dict, num_cols)
                    if (compare_col != None):
                        compare_val = self.getCompareVal(querywords[i:])

                    if (compare_col != None and compare_val != None):
                        wherecols.append(compare_col + " " + cid + " " + compare_val)

            agg_col = None
            for aid, aval in sql_agg_dict.items():
                if q in aval:
                    agg_col = self.getAggColumn(querywords[i:], sql_col_dict, num_cols)
                    print("agg_col", agg_col)
                    if (agg_col != None):
                        # myquery.append(aid+"("+agg_col+")")
                        aggcols.append(agg_col)
                        selectcols.append(aid + "(" + agg_col + ")")

        if (len(selectcols) == 0):
            selectcols.append(" * ")

        partial_query = "select "

        partial_query = partial_query + " , ".join(selectcols)

        partial_query = partial_query + " from [tablename] "

        if (len(wherecols) > 0):
            partial_query = partial_query + " where "
            partial_query = partial_query + " and ".join(wherecols)

        return partial_query