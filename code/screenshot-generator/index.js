const canvas = require('canvas');
const { JSDOM } = require('jsdom');
const Chart = require('chart.js');
const C2S = require('canvas2svg');
const xmlserializer = require('xmlserializer');
const chartConfig = require('./chartConfig');
const fs = require('fs')

C2S.prototype.getContext = function (contextId) {
    if (contextId == "2d" || contextId == "2D") {
        return this;
    }
    return null;
}

C2S.prototype.__parseFont = function () {
    const fontData = /^(\S+) (\S+) (.*)$/.exec(this.font);
    return {
        style: 'normal',
        size: fontData[2],
        family: fontData[3],
        weight: fontData[1],
        decoration: 'normal',
        href: null
    };
};

C2S.prototype.getSerializedSvg = function (fixNamedEntities) {
    var serialized = xmlserializer.serializeToString(this.__root),
        keys, i, key, value, regexp, xmlns;

    //IE search for a duplicate xmnls because they didn't implement setAttributeNS correctly
    xmlns = /xmlns="http:\/\/www\.w3\.org\/2000\/svg".+xmlns="http:\/\/www\.w3\.org\/2000\/svg/gi;
    if (xmlns.test(serialized)) {
        serialized = serialized.replace('xmlns="http://www.w3.org/2000/svg', 'xmlns:xlink="http://www.w3.org/1999/xlink');
    }

    if (fixNamedEntities) {
        keys = Object.keys(namedEntities);
        //loop over each named entity and replace with the proper equivalent.
        for (i = 0; i < keys.length; i++) {
            key = keys[i];
            value = namedEntities[key];
            regexp = new RegExp(key, "gi");
            if (regexp.test(serialized)) {
                serialized = serialized.replace(regexp, value);
            }
        }
    }

    return serialized;
};

const ctx = new C2S({
    width: 1000,
    height: 500,
    document: new JSDOM().window.document
});

new Chart(ctx, chartConfig);

console.log(ctx.getSerializedSvg());
