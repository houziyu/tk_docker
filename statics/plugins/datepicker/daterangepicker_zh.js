/*
  汉化daterangepicker封装,
  author:夏尔,
    个人网站:4xiaer.com（建设中）
  date:2017-08-29;
*/


//调用该方法即可，参数是触发元素，自定义配置对象，时间选择完成之后执行的回调方法
function daterangepicker_zh(Selector, options,cb) {
  var ele = $(Selector);
  
  set_options(options);

  function set_options(options) {
    var data = {};
    data.locale = {
      "format": 'YYYY-MM-DD',
      "separator": "至",
      "applyLabel": "确定",
      "cancelLabel": "取消",
      "fromLabel": "起始时间",
      "toLabel": "结束时间'",
      "customRangeLabel": "手动选择",
      "weekLabel": "W",
      "daysOfWeek": ["日", "一", "二", "三", "四", "五", "六"],
      "monthNames": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
      "firstDay": 1
    };

    data.ranges = {
      //'最近1小时': [moment().subtract('hours',1), moment()],
      '今日': [moment().startOf('day'), moment()],
      '昨日': [moment().subtract('days', 1).startOf('day'), moment().subtract('days', 1).endOf('day')],
      '最近7日': [moment().subtract('days', 6), moment()],
      '最近30日': [moment().subtract('days', 29), moment()],
      '本月': [moment().startOf("month"), moment().endOf("month")],
      '上个月': [moment().subtract(1, "month").startOf("month"), moment().subtract(1, "month").endOf("month")]
    };

    if (typeof options !== 'object' || options === null) {
      options = {}
      var new_options = $.extend(options, data);
    } else {
      var new_options = $.extend(options, data);
    }

    if (cb) {
      ele.daterangepicker(new_options,cb);
    } else {
      ele.daterangepicker(new_options);
    }
    
  }
}

