from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter


class IndeedWebscraperPipeline:
    def __init__(self):
        self.info = set()

    def process_item(self, item, spider):
        if str(item['info']) in self.info:
            raise DropItem("Duplicate job found: %s" % item)
        else:
            self.info.add(str(item['info']))
            return item

class JsonPipeline(object):
    def __init__(self):
        self.file = open("new_jobs.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
