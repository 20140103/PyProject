class CircleQueue{
     
    // var _buffer = Buffer.alloc(bufferLength || 512);//new Buffer(bufferLength || 512);//Buffer大于8kb 会使用slowBuffer，效率低 循环队列
    constructor(bufferLength){
        
        this._buffer = Buffer.alloc(bufferLength || 512);
        this._queueLen = this._buffer.length;
        this._readOffset = 0
        this._writeOffset = 0
    }
    /**
     * 
     * 可以读长度
     */
    getReadableLen() {
        if(this._writeOffset >= this._readOffset){
            return this._writeOffset - this._readOffset;
        }else{
            return this._queueLen - (this._readOffset - this._writeOffset);
        }
    }
    /**
     * 可以写长度
     */
    getWriteableLen(){
        if(this._writeOffset < this._readOffset){
            return this._readOffset - this._writeOffset;
        }else{
            return this._queueLen - (this._writeOffset - this._readOffset);
        }
    }
    /**
     * 读取数据 并丢失读取位置的数据
     * @param {起始位置} offset 
     * @param {读取长度} len 
     */
    readBuffer(len){
        if(this.getReadableLen()<len){
            console.log("读取数据长度超过了队列中可以读取数据的长度");
            return ;
        }
        if(len <= this._queueLen - this._readOffset ){
            var temp = Buffer.alloc(len);
            this._buffer.copy(temp,0,this._readOffset,this._readOffset + len)
            this._readOffset += len;
            return temp;
            // buf.copy(targetBuffer[, targetStart[, sourceStart[, sourceEnd]]])
        }else{
            //
            var temp = Buffer.alloc(len);
            var rlen = this._queueLen - this._readOffset
            this._buffer.copy(temp,0,this._readOffset,this._readOffset+rlen);//
            this._buffer.copy(temp,rlen,0,len -  rlen);
            this._readOffset = (len -  rlen);
            return temp;
        }
    }
    /**
     * 获取数据 但不清除数据
     * @param {获取数据} len 
     */
    getBuffer(len){
        if(this.getReadableLen()<len){
            console.log("读取数据长度超过了队列中可以读取数据的长度");
            return ;
        }
        if(len <= this._queueLen - this._readOffset ){
            var temp = Buffer.alloc(len);
            this._buffer.copy(temp,0,this._readOffset,this._readOffset + len)
            // this._readOffset += len;
            return temp;
            // buf.copy(targetBuffer[, targetStart[, sourceStart[, sourceEnd]]])
        }else{
            //
            var temp = Buffer.alloc(len);
            var rlen = this._queueLen - this._readOffset
            this._buffer.copy(temp,0,this._readOffset,this._readOffset + rlen);//
            this._buffer.copy(temp,rlen,0,len -  rlen);
            // this._readOffset += (len -  rlen);
            return temp;
        }
    }
    /**
     * 写入数据到循环队列中
     * @param {待写入数据} data 
     * @param {待写入数据长度} len 
     */
    writeBuffer(data,len){
        // console.log('writeBuffer len:'+len);
        if(len >this.getWriteableLen()){
            console.log("写入数据长度超过了队列中可以写入数据的长度 len:"+len);
            this.expansion(len)//扩容
            // return false;
        }
        if(len <= this._queueLen - this._writeOffset ){
            data.copy(this._buffer,this._writeOffset,0,len);//
            this._writeOffset += len
            return true;
        }else{
            var rlen = this._queueLen - this._writeOffset;
            data.copy(this._buffer,this._writeOffset,0,rlen);//
            data.copy(this._buffer,0,rlen,len);//
            this._writeOffset = len - rlen;
            return true;
        }
    }
    expansion(len){
        var ex = Math.ceil((Math.abs(len - this.getWriteableLen()) / 1024));//每次扩展1kb
        var tmp = new Buffer.alloc(ex * 1024);
        // var exlen = tmp.length - this._buffer.length;//增加的长度
        // this._buffer = Buffer.concat([this._buffer,tmp]);


        this._buffer = tmp;
        this._queueLen = this._buffer.length;
    }
    /**
     * 获取循环队列长度
     */
    getQuereLen(){
        return this._queueLen
    }
    
}
module.exports = CircleQueue;