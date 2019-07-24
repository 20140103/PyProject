
// var CircleQueue = require('./CircleQueue.1.js');

// var circleQueue = new CircleQueue(200);
// console.error(circleQueue.getQuereLen());
// var testBuffer = Buffer.alloc(80,1);//new Buffer(80);//
// var length = testBuffer.length;
// var i = 0;
// while(i < 10){
// console.error("写入testBuffer:"+Bytes2HexString(testBuffer));
// circleQueue.writeBuffer(testBuffer,length)
// // console.error("getReadableLen:"+circleQueue.getReadableLen());
// // console.error("getWriteableLen:"+circleQueue.getWriteableLen());
// // console.error("getQuereLen:"+circleQueue.getQuereLen());
// console.error("读出testBuffer:"+Bytes2HexString(circleQueue.readBuffer(length)));

// // console.error("getReadableLen:"+circleQueue.getReadableLen());
// // console.error("getWriteableLen:"+circleQueue.getWriteableLen());
// // console.error("getQuereLen:"+circleQueue.getQuereLen());
// i++;
// }

var json = '{"id":-1,"code":"BT"}'
var headBuffer = new Buffer(json.length);
headBuffer.write(json, 0, json.length, 'utf8');
// headBuffer['writeUInt32BE'](20,0,4);
// // headBuffer.writeIntBE(20,0,4);
// headBuffer['writeUInt32BE'](20,0,4);

// headBuffer['writeUInt32BE'](20,0,4);

// headBuffer['writeUInt32BE'](20,0,4);

// headBuffer['writeUInt32BE'](20,0,4);
// headBuffer.writeIntBE(200,4,4);
// headBuffer.writeIntBE(6,8,4);
// headBuffer.writeIntBE(-1,12,4);
// headBuffer.writeIntBE(0,16,4);
console.log(headBuffer.toJSON())
console.error("getQuereLen:"+Bytes2HexString(headBuffer));
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