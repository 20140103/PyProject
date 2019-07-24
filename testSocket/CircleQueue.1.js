var CircleQueue = function(bufferLength){
    var _buffer = new Buffer(bufferLength || 512);
    var _queueLen = _buffer.length;
    var _readOffset = 0
    var _writeOffset = 0

    /**
 * 
 * 可以读长度
 */
this.getReadableLen = function getReadableLen() {
    if(_writeOffset >= _readOffset){
        return _writeOffset - _readOffset;
    }else{
        return _queueLen - (_readOffset - _writeOffset);
    }
}
/**
 * 可以写长度
 */
this.getWriteableLen = function getWriteableLen(){
    if(_writeOffset < _readOffset){
        return _readOffset - _writeOffset;
    }else{
        return _queueLen - (_writeOffset - _readOffset);
    }
}
/**
 * 读取数据 并丢失读取位置的数据
 * @param {起始位置} offset 
 * @param {读取长度} len 
 */
this.readBuffer = function readBuffer(len){
    if(this.getReadableLen()<len){
        console.log("读取数据长度超过了队列中可以读取数据的长度 this.getReadableLen():"+this.getReadableLen() + " len:"+len);

        console.log("readBuffer 11111 _writeOffset:"+_writeOffset + " _readOffset:"+_readOffset);
        return [];
    }
    if(len <= _queueLen - _readOffset ){
        var temp = new Buffer(len);
        _buffer.copy(temp,0,_readOffset,_readOffset + len)
        _readOffset += len;
        console.log("readBuffer 11111 _writeOffset:"+_writeOffset + " _readOffset:"+_readOffset);
        return temp;
        // buf.copy(targetBuffer[, targetStart[, sourceStart[, sourceEnd]]])
    }else{
        //
        var temp = new Buffer(len);
        var rlen = _queueLen - _readOffset
        _buffer.copy(temp,0,_readOffset,_readOffset+rlen);//
        _buffer.copy(temp,rlen,0,len -  rlen);
        _readOffset = (len -  rlen);
        console.log("readBuffer 22222 _writeOffset:"+_writeOffset + " _readOffset:"+_readOffset);
        return temp;
    }
}
/**
 * 获取数据 但不清除数据
 * @param {获取数据} len 
 */
this.getBuffer = function getBuffer(len){
    if(this.getReadableLen()<len){
        console.log("读取数据长度超过了队列中可以读取数据的长度");
        return ;
    }
    if(len <= _queueLen - _readOffset ){
        var temp = new Buffer(len);
        _buffer.copy(temp,0,_readOffset,_readOffset + len)
        // _readOffset += len;
        return temp;
        // buf.copy(targetBuffer[, targetStart[, sourceStart[, sourceEnd]]])
    }else{
        //
        var temp = new Buffer(len);
        var rlen = _queueLen - _readOffset
        _buffer.copy(temp,0,_readOffset,_readOffset + rlen);//
        _buffer.copy(temp,rlen,0,len -  rlen);
        // _readOffset += (len -  rlen);
        return temp;
    }
}
/**
 * 写入数据到循环队列中
 * @param {待写入数据} data 
 * @param {待写入数据长度} len 
 */
this.writeBuffer = function writeBuffer(data,len){
    // console.log('writeBuffer len:'+len);
    if(len >this.getWriteableLen()){
        console.log("写入数据长度超过了队列中可以写入数据的长度 len:"+len);
        this.expansion(len)//扩容

        console.log("writeBuffer 22222 _writeOffset:"+_writeOffset + " _readOffset:"+_readOffset);
        // return false;
    }
    if(len <= _queueLen - _writeOffset ){
        data.copy(_buffer,_writeOffset,0,len);//
        _writeOffset += len
        console.log("writeBuffer 00000 _writeOffset:"+_writeOffset + " _readOffset:"+_readOffset) ;
        return true;
    }else{
        var rlen = _queueLen - _writeOffset;
        data.copy(_buffer,_writeOffset,0,rlen);//
        data.copy(_buffer,0,rlen,len);//
        _writeOffset = len - rlen;
        console.log("writeBuffer 11111 _writeOffset:"+_writeOffset + " _readOffset:"+_readOffset);
        return true;
    }
}
this.expansion =function expansion(len){
    var ex = Math.ceil((Math.abs(len - this.getWriteableLen()) / 1024));//每次扩展1kb
    var tmp = new Buffer(ex * 1024);
    // var exlen = tmp.length - _buffer.length;//增加的长度
    // _buffer = Buffer.concat([_buffer,tmp]);
    if(_readOffset < _writeOffset){
        _buffer.copy(tmp,0,_readOffset,_writeOffset);
    }else{
        _buffer.copy(tmp,0,_readOffset,_queueLen);
        _buffer.copy(tmp,_queueLen - _readOffset,0,_writeOffset);
    }
    _readOffset = 0;
    _writeOffset = this.getReadableLen();
    _buffer = tmp;
    _queueLen = _buffer.length;
}
/**
 * 获取循环队列长度
 */
this.getQuereLen = function getQuereLen(){
    return _queueLen
}
};

module.exports = exports = CircleQueue;