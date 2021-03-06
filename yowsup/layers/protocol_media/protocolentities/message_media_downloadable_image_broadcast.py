import time

from yowsup.common import YowConstants
from yowsup.structs import ProtocolTreeNode
from .message_media_downloadable_image import ImageDownloadableMediaMessageProtocolEntity

class BroadcastImageDownloadableMediaMessage(ImageDownloadableMediaMessageProtocolEntity):

    def __init__(self,
            mimeType, fileHash, url, ip, size, fileName,
            encoding, width, height, caption = None, mediaKey = None,
            _id = None, _from = None, jids = None, notify = None, timestamp = None,
            participant = None, preview = None, offline = None, retry = None):

        broadcastTime = int(time.time() * 1000)
        to = "%s@%s" % (broadcastTime,YowConstants.WHATSAPP_BROADCAST_SERVER)
        super(BroadcastImageDownloadableMediaMessage, self).__init__(
            mimeType, fileHash, url, ip, size, fileName,
            encoding, width, height, caption, mediaKey,
            _id, _from, to, notify, timestamp, participant,
            preview, offline, retry)
        self.setBroadcastProps(jids)

    def setBroadcastProps(self, jids):
        assert type(jids) is list, "jids must be a list, got %s instead." % type(jids)
        self.jids = jids

    def toProtocolTreeNode(self):
        node = super(BroadcastImageDownloadableMediaMessage, self).toProtocolTreeNode()
        toNodes = [ProtocolTreeNode("to", {"jid": jid}) for jid in self.jids]
        broadcastNode = ProtocolTreeNode("broadcast", children = toNodes)
        node.addChild(broadcastNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = ImageDownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = BroadcastImageDownloadableMediaMessage
        jids = [toNode.getAttributeValue("jid") for toNode in node.getChild("broadcast").getAllChildren()]
        entity.setBroadcastProps(jids)
        return entity

    @staticmethod
    def fromFilePath(path, url, ip, jids, mimeType = None, caption = None, dimensions = None):
        broadcastTime = int(time.time() * 1000)
        to = "%s@%s" % (broadcastTime,YowConstants.WHATSAPP_BROADCAST_SERVER)
        entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(
            path, url, ip, to, mimeType, caption, dimensions)
        entity.__class__ = BroadcastImageDownloadableMediaMessage
        entity.setBroadcastProps(jids)
        return entity
