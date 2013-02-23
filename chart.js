$(document).ready(function () {
  Highcharts.setOptions({global: {useUTC: false}});
  var chart = new Highcharts.Chart({
        chart: {
          renderTo: 'chart',
          defaultSeriesType: 'areaspline',
        },
        title: {
          text: 'Hacker News Front Page and New Page Scores'
        },
        xAxis: {
          type: 'datetime'
        },
        yAxis: {
          minPadding: 0.2,
          maxPadding: 0.2,
          title: {
            text: 'Points'
          }
        },
        series: [
        { name: 'Highest New', data: [] },
        { name: 'Lowest front page', data: []}
        ]
    }
  )
  chart.showLoading();

  var score_db = new Firebase('https://hn-notify-prod.firebaseio.com/scores');

  // Only show the past 12 hours, to improve chart load time
  var start_time = (new Date().getTime() / 1000) - 60*60*12;

  score_db.startAt(start_time).on('child_added', function (db_update) {
    var scores = db_update.val();

    //Shift if there's more than ~two days of data
    var series = chart.series[0],
        shift = series.data.length > 1500;

    // Javascript time is unix time * 1000
    chart.series[0].addPoint([scores['time'] * 1000, scores['new']], true, shift);
    chart.series[1].addPoint([scores['time'] * 1000, scores['front']], true, shift);

    chart.hideLoading();
  });
});
