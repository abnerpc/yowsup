import time

from yowsup.common import YowConstants
from yowsup.structs import ProtocolTreeNode
from .message_media_downloadable_audio import AudioDownloadableMediaMessageProtocolEntity

class BroadcastAudioDownloadableMediaMessage(AudioDownloadableMediaMessageProtocolEntity):

    def __init__(self,
            mimeType, fileHash, url, ip, size, fileName,
            abitrate, acodec, asampfreq, duration, encoding, origin, seconds, mediaKey = None,
            _id = None, _from = None, jids = None, notify = None, timestamp = None,
            participant = None, preview = None, offline = None, retry = None):

        broadcastTime = int(time.time() * 1000)
        to = "%s@%s" % (broadcastTime,YowConstants.WHATSAPP_BROADCAST_SERVER)
        super(BroadcastAudioDownloadableMediaMessage, self).__init__(
            mimeType, fileHash, url, ip, size, fileName,
            abitrate, acodec, asampfreq, duration, encoding, origin, seconds, mediaKey,
            _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        self.setBroadcastProps(jids)

    def setBroadcastProps(self, jids):
        assert type(jids) is list, "jids must be a list, got %s instead." % type(jids)
        self.jids = jids

    def toProtocolTreeNode(self):
        node = super(BroadcastAudioDownloadableMediaMessage, self).toProtocolTreeNode()
        toNodes = [ProtocolTreeNode("to", {"jid": jid}) for jid in self.jids]
        broadcastNode = ProtocolTreeNode("broadcast", children = toNodes)
        node.addChild(broadcastNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = AudioDownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = BroadcastAudioDownloadableMediaMessage
        jids = [toNode.getAttributeValue("jid") for toNode in node.getChild("broadcast").getAllChildren()]
        entity.setBroadcastProps(jids)
        return entity

    @staticmethod
    def fromFilePath(path, url, ip, jids, mimeType = None, preview = None, filehash = None, filesize = None):
        broadcastTime = int(time.time() * 1000)
        to = "%s@%s" % (broadcastTime,YowConstants.WHATSAPP_BROADCAST_SERVER)
        entity = AudioDownloadableMediaMessageProtocolEntity.fromFilePath(
            path, url, ip, to, mimeType, preview, filehash, filesize)
        entity.__class__ = BroadcastAudioDownloadableMediaMessage
        entity.setBroadcastProps(jids)
        return entity
