var net = require('net');

var HOST = '0.0.0.0';
var PORT = 8081;
var bufferLength = 512
var _buffer = Buffer.alloc(bufferLength || 512);//new Buffer(bufferLength || 512);//Buffer大于8kb 会使用slowBuffer，效率低 循环队列
var _readOffset = 0;
var _putOffset = 0;
var CircleQueue = require('./CircleQueue.1.js');

var circleQueue = new CircleQueue(bufferLength);
var msock;

//mars
var startIndex = 0;
var versionIndex = startIndex + 4;
var cmdidIndex = versionIndex + 4;
var seqIndex = cmdidIndex + 4;
var bodyLenIndex = seqIndex + 4;

//ctf
var ctfHeadFlagIndex = bodyLenIndex + 4;
var ctfHeadFlagLen = 3;

var _protocolHead = "CFT"
// var _buffer = new Buffer(512);//Buffer大于8kb 会使用slowBuffer，效率低

// 创建一个TCP服务器实例，调用listen函数开始监听指定端口
// 传入net.createServer()的回调函数将作为”connection“事件的处理函数
// 在每一个“connection”事件中，该回调函数接收到的socket对象是唯一的
net.createServer(function (sock) {

    // 我们获得一个连接 - 该连接自动关联一个socket对象
    console.log('CONNECTED: ' +
        sock.remoteAddress + ':' + sock.remotePort);
    msock = sock;
    // 为这个socket实例添加一个"data"事件处理函数
    sock.on('data', function (data) {
        // 回发该数据，客户端将收到来自服务端的数据
        // sock.write(data);
        // var tem = Buffer.alloc(data.length,data)
        put(data, data.length)
    });

    // 为这个socket实例添加一个"close"事件处理函数
    sock.on('close', function (data) {
        console.log('CLOSED: ' +
            sock.remoteAddress + ' ' + sock.remotePort);
    });

}).listen(PORT, HOST);

function bin2String(array) {
    var result = "";
    for (var i = 0; i < array.length; i++) {
        result += String.fromCharCode(parseInt(array[i], 2));
    }
    return result;
}

console.log('Server listening on ' + HOST + ':' + PORT);

function Bytes2HexString(arrBytes) {
    var str = "";
    for (var i = 0; i < arrBytes.length; i++) {
        var tmp;
        var num = arrBytes[i];
        if (num < 0) {
            //此处填坑，当byte因为符合位导致数值为负时候，需要对数据进行处理
            tmp = (255 + num + 1).toString(16);
        } else {
            tmp = num.toString(16);
        }
        if (tmp.length == 1) {
            tmp = "0" + tmp;
        }
        str += tmp + ' ';
    }
    return str;
}
function proc(circleQueue) {
    do {
        if (circleQueue.getReadableLen() < 20) {
            console.log('数据长度不够 ')
            // break;//连包头都读不了
        } else {
            //获取mars包头byte数组
            var headBuffer = circleQueue.getBuffer(20)
            console.log('DATA ' + 'headBuffer: ' + Bytes2HexString(headBuffer));
            //mars head
            headLen = headBuffer.readUInt32BE(startIndex)
            version = headBuffer.readUInt32BE( versionIndex)
            cmdid = headBuffer.readUInt32BE(cmdidIndex)
            seq = headBuffer.readInt32BE(seqIndex)
            bodyLen = headBuffer.readUInt32BE(bodyLenIndex)
            
            if(version != 200){
                //协议版本是不是对的
                console.error("协议版本不对 version:"+version);
                // msock.close();
                return;
            }
            //这两种情况都表示数据异常了 我们只能关闭socket
            if( bodyLen <= 0 || bodyLen > 2048){
                console.error("protocol 长度不对 bodyLen:"+bodyLen);
                // msock.close();
                 return;
            }
            // headBuffer.writeIntBE()
            console.log('headLen:' + headLen + ' version:' + version + ' cmdid:' + cmdid + ' seq:' + seq + " bodyLen:" + bodyLen);
            // data.
            // ctf
            if (circleQueue.getReadableLen() >= 8 + 20) {
                var bodyHeadBuffer = circleQueue.getBuffer(8 + 20)
                
                console.log('DATA ' + 'bodyHeadBuffer: ' + Bytes2HexString(bodyHeadBuffer));
                
                var ctfHeadFlag = bodyHeadBuffer.toString('utf8', ctfHeadFlagIndex, ctfHeadFlagIndex + ctfHeadFlagLen)
                var ctfBodyLen = bodyHeadBuffer.readInt16BE(ctfHeadFlagIndex + 3)
                var ctfDataType = bodyHeadBuffer.readUInt8(ctfHeadFlagIndex + 5)
                var ctfBodyLength = bodyHeadBuffer.readInt16BE(ctfHeadFlagIndex + 6)
                console.log(' ctfHeadFlag:' + ctfHeadFlag + ' ctfBodyLen:' + ctfBodyLen + ' ctfDataType:' + ctfDataType + ' ctfBodyLength:' + ctfBodyLength);
                
                //cft 标志位错误
                if (ctfHeadFlag !== _protocolHead) {
                    console.error("protocol head error ctfHeadFlag:"+ctfHeadFlag);
                    // msock.close();
                    return ;//self.emit("error", new Error('protocol head error:' + headFlag));
                }
                if (ctfBodyLen > 0 && circleQueue.getReadableLen() >= ctfBodyLen + 20 + 5) {
                    var bodyBuffer = circleQueue.readBuffer(bodyLen + 20)
                    console.log('DATA ' + 'bodyBuffer: ' + Bytes2HexString(bodyBuffer));
                    if (ctfBodyLen <= bodyBuffer.length) {
                        console.log('DATA ' + ': ' + bodyBuffer.toString('utf8', 20 + 8, ctfBodyLength + 20 + 8));
                    }
                    msock.write(bodyBuffer);
                }
            } else {
                // circleQueue.readBuffer(20)
                msock.write(headBuffer);
            }
            // // 回发该数据，客户端将收到来自服务端的数据
            // sock.write(data);
        }
    } while (circleQueue.getReadableLen() >= 20);

}
function put(buffer, len) {
    // proc(buffer);

    circleQueue.writeBuffer(buffer, len);
    // console.error(circleQueue.getReadableLen());
    // circleQueue.readBuffer(len)
    console.log('DATA ' + 'writeBuffer: ' + Bytes2HexString(buffer));
    // console.log('DATA ' + 'put: ' + Bytes2HexString(circleQueue.readBuffer(len)));
    // console.error(circleQueue.getReadableLen());
    proc(circleQueue);
};