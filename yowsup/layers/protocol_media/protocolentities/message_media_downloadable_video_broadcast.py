import time

from yowsup.common import YowConstants
from yowsup.structs import ProtocolTreeNode
from .message_media_downloadable_video import VideoDownloadableMediaMessageProtocolEntity


class BroadcastVideoDownloadableMediaMessage(VideoDownloadableMediaMessageProtocolEntity):

    def __init__(self,
                 mimeType, fileHash, url, ip, size, fileName,
                 abitrate, acodec, asampfmt, asampfreq, duration, encoding, fps,
                 width, height, seconds, vbitrate, vcodec, caption=None, mediaKey = None,
                 _id=None, _from=None, jids=None, notify=None, timestamp=None,
                 participant=None, preview=None, offline=None, retry=None):

        broadcastTime = int(time.time() * 1000)
        to = "%s@%s" % (broadcastTime,YowConstants.WHATSAPP_BROADCAST_SERVER)
        super(BroadcastVideoDownloadableMediaMessage, self).__init__(
            mimeType, fileHash, url, ip, size, fileName,
            abitrate, acodec, asampfmt, asampfreq, duration, encoding, fps,
            width, height, seconds, vbitrate, vcodec, caption, mediaKey,
            _id, _from, to, notify, timestamp,
            participant, preview, offline, retry)
        self.setBroadcastProps(jids)

    def setBroadcastProps(self, jids):
        assert type(jids) is list, "jids must be a list, got %s instead." % type(jids)
        self.jids = jids

    def toProtocolTreeNode(self):
        node = super(BroadcastVideoDownloadableMediaMessage, self).toProtocolTreeNode()
        toNodes = [ProtocolTreeNode("to", {"jid": jid}) for jid in self.jids]
        broadcastNode = ProtocolTreeNode("broadcast", children = toNodes)
        node.addChild(broadcastNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = VideoDownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = BroadcastVideoDownloadableMediaMessage
        jids = [toNode.getAttributeValue("jid") for toNode in node.getChild("broadcast").getAllChildren()]
        entity.setBroadcastProps(jids)
        return entity

    @staticmethod
    def fromFilePath(path, url, ip, jids, mimeType=None, caption=None):
        broadcastTime = int(time.time() * 1000)
        to = "%s@%s" % (broadcastTime,YowConstants.WHATSAPP_BROADCAST_SERVER)
        entity = VideoDownloadableMediaMessageProtocolEntity.fromFilePath(
            path, url, ip, to, mimeType, caption)
        entity.__class__ = BroadcastVideoDownloadableMediaMessage
        entity.setBroadcastProps(jids)
        return entity
