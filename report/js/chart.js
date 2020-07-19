class Chart {
    constructor(SOI, id, width, height, margin) {
        // console.log(SOI);
        this.SOIDimension = SOI.dimension(function(SOI) {
            return SOI.category;
        });
        // console.log(this.SOIDimension.top(Infinity));
        this.chartContainer = d3.select(id);
        this.chart = null; // This will hold chart SVG Dom element reference
        this.chartWidth = width; // Width in pixels
        this.chartHeight = height; // Height in pixels
        this.margin = margin; // Margin in pixels
        this.chartHeightWithoutMargin = this.chartHeight - this.margin;
        this.chartWidthWithoutMargin = this.chartWidth - this.margin;
        this.xScale = null;
        this.yScale = null;
        this.tooltipContainer = null;
        this.xMax = 5;
    }

    rowChart() {
        this.createSvg();
        this.initScales();
        this.drawAxes();
        this.drawBar();
    }

    ratioChart() {
        this.createSvg();
        this.drawRatio();
    }

    createSvg() {
        this.chart = this.chartContainer
            .append('svg')
            .attr('width', this.chartWidth)
            .attr('height', this.chartHeight);
    }

    initScales() {
        // console.log(+this.chart.attr('width'));
        let chartWidth = +this.chart.attr('width') - this.margin;
        let chartHeight = +this.chart.attr('height') - this.margin;

        // Adjust Scale Appearance
        let yDomain = this.SOIDimension.top(Infinity).map((d) => {return d.category});
        yDomain.unshift("");
        yDomain.push("");

        // generate ordinal yRange
        let interval = (chartHeight - this.margin) / (this.SOIDimension.top(Infinity).length + 1);
        let yRange = [];
        for (let pos = chartHeight; pos >= this.margin; pos -= interval) {
            yRange.push(pos);
        }

        // Adding xMax if out of range
        function findMax (data) {
            let max = 0;
            for (i in data) max = data[i]['count'] > max ? data[i]['count'] : max;
            return max;
        }
        while (findMax(this.SOIDimension.top(Infinity)) > this.xMax)
            this.xMax += 5;

        this.xScale = d3.scaleLinear().domain([0, this.xMax]).range([this.margin, chartWidth]);
        this.yScale = d3.scaleOrdinal().domain(yDomain).range(yRange);
    }

    drawAxes() {
        let format = d3.format('.0f');
        let xAxis = d3.axisBottom(this.xScale).tickFormat(format).ticks(this.xMax);
        let yAxis = d3.axisLeft(this.yScale);

        this.chart
            .append('g')
            .attr('class', 'c-axis')
            .attr('transform', 'translate(' + this.margin + ', 0)')
            .call(yAxis)
            .append('g')
            .append('text')
            .attr("fill", "currentColor")
            .attr('x', '10')
            .attr('dy', '4em')
            .attr('font-size', 'larger')
            .text("類別");

        this.chart
            .append('g')
            .attr('class', 'c-axis')
            .attr('transform', 'translate(0, ' + this.chartHeightWithoutMargin + ')')
            .call(xAxis)
            .append('g')
            .append('text')
            .attr("fill", "currentColor")
            .attr('x', (this.margin + this.chartWidthWithoutMargin) / 2)
            .attr('dy', '3em')
            .attr('font-size', 'larger')
            .text("待改進數量");
    }

    drawBar() {

        let line = d3.line()
            .x((d) => {
                return this.yScale(d.category);
            })
            .y((d) => {
                return this.xScale(d.count);
            });

        // bar
        this.chart.selectAll()
            .data(this.SOIDimension.top(Infinity))
            .enter()
            .append('rect')
            .attr('class', 'c-bar')
            .attr('y', (d) => { return this.yScale(d.category) - this.chartHeightWithoutMargin / 24; })
            .attr('x', (d) => this.margin + 1)
            .attr('width', (d) => this.xScale(d.count) - this.margin)
            .attr('height', () => this.chartHeightWithoutMargin / 12)
            .on('mouseover', (d) => {
                this.showTooltip(
                    d.category + ':  ' + d.count,
                    d3.event.pageX,
                    d3.event.pageY
                );
            })
            .on('mouseout', (d) => {
                this.hideTooltip();
            })
            .on('mousemove', (d) => {
                this.hideTooltip();
                this.showTooltip(
                    d.category + ':  ' + Math.round(d.count * 100) / 100,
                    d3.event.pageX,
                    d3.event.pageY
                );
            });

    }

    drawRatio() {
        let line = d3.line()
            .x((d) => {
                return this.yScale(d.cat);
            })
            .y((d) => {
                return this.xScale(d.number);
            });


        // bar
        this.chart.selectAll()
            .data(this.SOIDimension.top(Infinity))
            .enter()
            .append('rect')
            .attr('class', (d) => (d.cat == 'uncheck' ? 'c-bar uncheck' : 'c-bar'))
            .attr('y', 0)
            .attr('x', (d) => this.margin + 1 + (d.cat == 'checked' ? 0 : 1) * this.chartWidthWithoutMargin * (1 - d.perc))
            .attr('width', (d) => this.chartWidthWithoutMargin * d.perc)
            .attr('height', () => this.chartHeightWithoutMargin)
            .on('mouseover', (d) => {
                this.showTooltip(
                    d.cat + ':  ' + d.number,
                    d3.event.pageX,
                    d3.event.pageY
                );
            })
            .on('mouseout', (d) => {
                this.hideTooltip();
            })
            .on('mousemove', (d) => {
                this.hideTooltip();
                this.showTooltip(
                    d.cat + ':  ' + Math.round(d.number * 100) / 100,
                    d3.event.pageX,
                    d3.event.pageY
                );
            });
    }

    createTooltipIfDoesntExist() {
        if (this.tooltipContainer !== null) {
            return;
        }

        this.tooltipContainer = this.chartContainer
            .append('div')
            .attr('class', 'c-tooltip')
    }

    showTooltip(content, left, top) {
        this.createTooltipIfDoesntExist();

        this.tooltipContainer
            .html(content)
            .style('left', left + 10 + 'px')
            .style('top', top - 50 + 'px')
            .style('background', (content.includes("uncheck") ? 'AntiqueWhite' : 'aliceblue'))
            .style('border-color', (content.includes("uncheck") ? '#dc3545' : '#2055b6'));

        this.tooltipContainer
            .transition()
            .duration(100)
            .style('opacity', 1);
    }

    hideTooltip() {
        this.createTooltipIfDoesntExist();

        this.tooltipContainer
            .transition()
            .duration(300)
            .style('opacity', 0);
    }
}

function loadChart() {
    var dataToRowChart = new Array;
    var chartWidth = $('#ratioChart').width();
    var county = $('#countySel1 option:selected').text()
    for (i in overallData[county]["TBD"]) {
        var temp = new Object;
        temp["category"] = i;
        temp["count"] = overallData[county]["TBD"][i];
        dataToRowChart.push(temp);
    }
    dataToRowChart = crossfilter(dataToRowChart);
    d3.selectAll(".c-chart > *").remove(); // Clear chart
    var rowChart = new Chart(dataToRowChart, '#overviewChart', width = chartWidth, height = 250, margin = 60);
    rowChart.rowChart();

    dataToRatio = crossfilter([{"cat": "checked", "number": +overallData[county]['checked_num'], 'perc': +overallData[county]['check_ratio']},
                               {"cat": "uncheck", "number": +overallData[county]['uncheck_num'], 'perc': 1 - +overallData[county]['check_ratio']}]);

    var ratioChart = new Chart(dataToRatio, '#ratioChart', width = chartWidth, height = 30, margin = 0);
    ratioChart.ratioChart();
}
