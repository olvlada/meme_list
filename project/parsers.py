import re
import xlrd


def _sanitize(value):
    return re.sub(u'\s*', '', value.lower().strip())


class RowParser(object):
    def parse(self, row):
        return {
            'domain': row.get('domain', 'Unknown'),
            'alexa_rank': int(row.get('alexarank', 0)),
            'verticals': self._parse_list(row.get('verticals', 'Unknown'), ','),
            'platforms': self._parse_list(row.get('platform', 'Unknown'), ','),
            'sizes': self._parse_list(row.get('size', 'Unknown'), ','),
            'geos': self._parse_list(row.get('geos', 'Unknown'), ','),
            'minimum_rate': float(row.get('minimumrate', 0.0))
        }

    def _parse_list(self, value, separator):
        return [{'name': item.strip()} for item in value.split(separator)]


class FileParser(object):
    def __init__(self, file, row_parser):
        self.file = file
        self.row_parser = row_parser

    def parse(self):
        book = xlrd.open_workbook(file_contents=self.file.read())
        sheet = book.sheet_by_index(0)
        headers = [_sanitize(item.value) for item in sheet.row(0)]

        result = []
        for row_index in xrange(1, sheet.nrows):
            row = sheet.row(row_index)
            mapped_row = {key: value.value for key, value in zip(headers, row)}
            result.append(self.row_parser.parse(mapped_row))

        return result
