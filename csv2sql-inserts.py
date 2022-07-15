""" generates SQL-INSERT-Commands

Usage: csv2sql-inserts.py [table-name] c:\temp\import.csv c:\temp\export.sql

version 0.1
"""
import csv
import sys
import os
import io


def main():
    if len(sys.argv) == 1:
        print(f"USAGE: {sys.argv[0]} table-name csv-input-file [sql-output-file]")
        quit()

    table_name = sys.argv[1]
    input_file = sys.argv[2]
    output_file = None
    if len(sys.argv) > 3:
        output_file = sys.argv[3]

    if input_file.endswith(".csv"):
        sourceFile = os.path.abspath(input_file)
        if os.path.exists(sourceFile):
            print(f"load....{sourceFile}")
        else:
            print(f"{input_file} existiert nicht")
            quit(1)


    if len(sourceFile)>0:
        table = table_name
        print(f"SourceFile: {sourceFile}")
        count = 0
        if output_file is not None:
            writer = io.open(output_file, "w", encoding="utf-8")

        with io.open(sourceFile, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                keys, values = "", ""
                for key in row:
                    if len(keys) > 0:
                        keys = keys + ', '
                    if "'" in key:
                        key = key.replace("'", "''")
                    if "[" in key:
                        key = key.replace("[", "_")
                    if "]" in key:
                        key = key.replace("]", "_")

                    keys = keys + f"[{key}]"

                for key in row:
                    if len(values)>0:
                        values = values + ', '

                    value = row[key]
                    if "'" in value:
                        value = value.replace("'", "''")
                    values = values + f"'{value}'"

                sql = f"INSERT INTO {table} ({keys}) VALUES ({values});"
                count += 1
                if output_file is not None:
                    writer.write(sql)
                    writer.write("\r\n")
                else:
                    print(sql)

        print("")
        print(f"{count} lines")

        if output_file is not None:
            writer.close()


if __name__ == "__main__":
    main()
