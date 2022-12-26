/**
 * dropload
 * Simon(http://ons.me/526.html)
 * 0.9.1(161205)
 */

;(function($){
    'use strict';
    var win = window;
    var doc = document;
    var $win = $(win);
    var $doc = $(doc);
    $.fn.dropload = function(options){
        return new MyDropLoad(this, options);
    };
    var MyDropLoad = function(element, options){
        var me = this;
        me.$element = element;
        // Whether to insert DOM above
        me.upInsertDOM = false;
        // loading status
        me.loading = false;
        // Is it locked
        me.isLockUp = false;
        me.isLockDown = false;
        // Is there data
        me.isData = true;
        me._scrollTop = 0;
        me._threshold = 0;
        me.init(options);
    };

    // initialization
    MyDropLoad.prototype.init = function(options){
        var me = this;
        me.opts = $.extend(true, {}, {
            scrollArea : me.$element,                                            // 滑动区域
            domUp : {                                                            // 上方DOM
                domClass   : 'dropload-up',
                domRefresh : '<div class="dropload-refresh">↓下拉刷新</div>',
                domUpdate  : '<div class="dropload-update">↑释放更新</div>',
                domLoad    : '<div class="dropload-load"><span class="loading"></span>加载中...</div>'
            },
            domDown : {                                                          // 下方DOM
                domClass   : 'dropload-down',
                domRefresh : '<div class="dropload-refresh">↑上拉加载更多</div>',
                domLoad    : '<div class="dropload-load"><span class="loading"></span>加载中...</div>',
                domNoData  : '<div class="dropload-noData">-- END --</div>'
            },
            autoLoad : true,                                                     // 自动加载
            distance : 50,                                                       // 拉动距离
            threshold : '',                                                      // 提前加载距离
            loadUpFn : '',                                                       // 上方function
            loadDownFn : ''                                                      // 下方function
        }, options);

        // If loading below, insert DOM below beforehand
        if(me.opts.loadDownFn != ''){
            me.$element.append('<div class="'+me.opts.domDown.domClass+'">'+me.opts.domDown.domRefresh+'</div>');
            me.$domDown = $('.'+me.opts.domDown.domClass);
        }

        // Calculate the advance loading distance
        if(!!me.$domDown && me.opts.threshold === ''){
// Load when sliding to 2/3 of the loading area by default            me._threshold = Math.floor(me.$domDown.height()*1/3);
        }else{
            me._threshold = me.opts.threshold;
        }

        // Determine the scroll area
        if(me.opts.scrollArea == win){
            me.$scrollArea = $win;
            // Get document height
            me._scrollContentHeight = $doc.height();
// Get the height of the win display area-there is a pit here            me._scrollWindowHeight = doc.documentElement.clientHeight;
        }else{
            me.$scrollArea = me.opts.scrollArea;
            me._scrollContentHeight = me.$element[0].scrollHeight;
            me._scrollWindowHeight = me.$element.height();
        }
        fnAutoLoad(me);

        // Window adjustment
        $win.on('resize',function(){
            clearTimeout(me.timer);
            me.timer = setTimeout(function(){
                if(me.opts.scrollArea == win){
                // Get the height of the win display area again
                me._scrollWindowHeight = win.innerHeight;
                }else{
                    me._scrollWindowHeight = me.$element.height();
                }
                fnAutoLoad(me);
            },150);
            
        });

        // Bound touch
        me.$element.on('touchstart',function(e){
            if(!me.loading){
                fnTouches(e);
                fnTouchstart(e, me);
            }
        });
        me.$element.on('touchmove',function(e){
            if(!me.loading){
                fnTouches(e, me);
                fnTouchmove(e, me);
            }
        });
        me.$element.on('touchend',function(){
            if(!me.loading){
                fnTouchend(me);
            }
        });

        // Load below
        me.$scrollArea.on('scroll',function(){
            me._scrollTop = me.$scrollArea.scrollTop();

            // Scrolling the page to trigger loading data
            if(me.opts.loadDownFn != '' && !me.loading && !me.isLockDown && (me._scrollContentHeight - me._threshold) <= (me._scrollWindowHeight + me._scrollTop)){
                loadDown(me);
            }
        });

        // Load the first page ahead of time
        loadDown(me);
    };

    // touches
    function fnTouches(e){
        if(!e.touches){
            e.touches = e.originalEvent.touches;
        }
    }

    // touchstart
    function fnTouchstart(e, me){
        me._startY = e.touches[0].pageY;
        // Remember the scrolltop value when touched
        me.touchScrollTop = me.$scrollArea.scrollTop();
    }

    // touchmove
    function fnTouchmove(e, me){
        me._curY = e.touches[0].pageY;
        me._moveY = me._curY - me._startY;

        if(me._moveY > 0){
            me.direction = 'down';
        }else if(me._moveY < 0){
            me.direction = 'up';
        }

        var _absMoveY = Math.abs(me._moveY);

        // Load above
        if(me.opts.loadUpFn != '' && me.touchScrollTop <= 0 && me.direction == 'down' && !me.isLockUp){
            e.preventDefault();

            me.$domUp = $('.'+me.opts.domUp.domClass);
            // If there is no DOM in the loading area
            if(!me.upInsertDOM){
                me.$element.prepend('<div class="'+me.opts.domUp.domClass+'"></div>');
                me.upInsertDOM = true;
            }
            
            fnTransition(me.$domUp,0);

            // drop down
            if(_absMoveY <= me.opts.distance){
                me._offsetY = _absMoveY;
                // todo: When moving, it will continue to empty and increase dom, which may affect performance, the same below
                me.$domUp.html(me.opts.domUp.domRefresh);
// Specified distance <drop-down distance <Specified distance*2            }else if(_absMoveY > me.opts.distance && _absMoveY <= me.opts.distance*2){
                me._offsetY = me.opts.distance+(_absMoveY-me.opts.distance)*0.5;
                me.$domUp.html(me.opts.domUp.domUpdate);
// drop-down distance> specified distance*2            }else{
                me._offsetY = me.opts.distance+me.opts.distance*0.5+(_absMoveY-me.opts.distance*2)*0.2;
            }

            me.$domUp.css({'height': me._offsetY});
        }
    }

    // touchend
    function fnTouchend(me){
        var _absMoveY = Math.abs(me._moveY);
        if(me.opts.loadUpFn != '' && me.touchScrollTop <= 0 && me.direction == 'down' && !me.isLockUp){
            fnTransition(me.$domUp,300);

            if(_absMoveY > me.opts.distance){
                me.$domUp.css({'height':me.$domUp.children().height()});
                me.$domUp.html(me.opts.domUp.domLoad);
                me.loading = true;
                me.opts.loadUpFn(me);
            }else{
                me.$domUp.css({'height':'0'}).on('webkitTransitionEnd mozTransitionEnd transitionend',function(){
                    me.upInsertDOM = false;
                    $(this).remove();
                });
            }
            me._moveY = 0;
        }
    }

// If the document height is not greater than the window height and the data is less, the data below will be automatically loaded    function fnAutoLoad(me){
        if(me.opts.loadDownFn != '' && me.opts.autoLoad){
            if((me._scrollContentHeight - me._threshold) <= me._scrollWindowHeight){
                loadDown(me);
            }
        }
    }

    // Regain the document height
    function fnRecoverContentHeight(me){
        if(me.opts.scrollArea == win){
            me._scrollContentHeight = $doc.height();
        }else{
            me._scrollContentHeight = me.$element[0].scrollHeight;
        }
    }

    // Load below
    function loadDown(me){
        me.direction = 'up';
        me.$domDown.html(me.opts.domDown.domLoad);
        me.loading = true;
        me.opts.loadDownFn(me);
    }

    // locking
    MyDropLoad.prototype.lock = function(direction){
        var me = this;
        // If you don't specify the direction
        if(direction === undefined){
            // If the operating direction is upward
            if(me.direction == 'up'){
                me.isLockDown = true;
            // If the operating direction is down
            }else if(me.direction == 'down'){
                me.isLockUp = true;
            }else{
                me.isLockUp = true;
                me.isLockDown = true;
            }
        // If you specify the lock above
        }else if(direction == 'up'){
            me.isLockUp = true;
        // If you specify the lock below
        }else if(direction == 'down'){
            me.isLockDown = true;
// In order to solve the tab effect bug in DEMO5, there is a bug because it slides to the bottom, then slides up to point tab, direction=down, so there is a bug            me.direction = 'up';
        }
    };

    // Unlock
    MyDropLoad.prototype.unlock = function(){
        var me = this;
        // Simple and crude to unlock
        me.isLockUp = false;
        me.isLockDown = false;
        // In order to solve the tab effect bug in DEMO5, because slide to the bottom, then slide up to point tab, direction=down, so there is a bug
        me.direction = 'up';
    };

    // no data
    MyDropLoad.prototype.noData = function(flag){
        var me = this;
        if(flag === undefined || flag == true){
            me.isData = false;
        }else if(flag == false){
            me.isData = true;
        }
    };

    // Reset
    MyDropLoad.prototype.resetload = function(){
        var me = this;
        if(me.direction == 'down' && me.upInsertDOM){
            me.$domUp.css({'height':'0'}).on('webkitTransitionEnd mozTransitionEnd transitionend',function(){
                me.loading = false;
                me.upInsertDOM = false;
                $(this).remove();
                fnRecoverContentHeight(me);
            });
        }else if(me.direction == 'up'){
            me.loading = false;
            // If there is data
            if(me.isData){
                // Loading area modification style
                me.$domDown.html(me.opts.domDown.domRefresh);
                fnRecoverContentHeight(me);
                fnAutoLoad(me);
            }else{
                // If there is no data
                me.$domDown.html(me.opts.domDown.domNoData);
            }
        }
    };

    // css transition 
    function fnTransition(dom,num){
        dom.css({
            '-webkit-transition':'all '+num+'ms',
            'transition':'all '+num+'ms'
        });
    }
})(window.Zepto || window.jQuery);