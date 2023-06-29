# self.item_list = ListWidget(self)
#
# # self.item_list = QListWidget(self)
#
# i = 0
# for stand in self.cp.list_items():
#     item = QListWidgetItem()
#     # item = SwitchableItem()
#     item.setData(Qt.UserRole, _qmimedata_to_dict(stand[1], self.cp.available_formats))
#
#     switch_item = SwitchableItem(stand[1].text(), 1)
#     i += 1
#
#     item.setSizeHint(QSize(100, 50))
#
#     self.item_list.addItem(item)
#     self.item_list.setItemWidget(item, switch_item)