package org.example;

import java.util.Date;
import java.util.HashMap;
import org.apache.flink.streaming.api.functions.windowing.ProcessAllWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

public class StatisticsStream extends ProcessAllWindowFunction<MessageFromTopic, TripDurationStatistics, TimeWindow> {

    @Override
    public void process(ProcessAllWindowFunction<MessageFromTopic, TripDurationStatistics, TimeWindow>.Context context,
                        Iterable<MessageFromTopic> elements, Collector  <TripDurationStatistics> out) throws Exception {
        float sum = 0;
        float max = 0;
        float min = 50000;
        float avg = 0;
        double stddev = 0;
        String street1 = "";
        int name1 = 0;
        String street2 = "";
        int name2 = 0;
        String street3 = "";
        int name3 = 0;
        float count = 0;

        HashMap<String, Integer> popular = new HashMap<>();

        for (MessageFromTopic msg : elements) {
            count ++;
            sum += msg.tripduration;
            if (msg.tripduration > max)
                max = msg.tripduration;
            if (msg.tripduration < min)
                min = msg.tripduration;
            if(!popular.containsKey(msg.end_station_name)) {
                popular.put(msg.end_station_name, 1);
            } else {
                int newValue = popular.get(msg.end_station_name) + 1;
                popular.replace(msg.end_station_name, newValue);
            }
        }
        avg = sum / count;

        street1 = (String) popular.keySet().toArray()[0];
        name1 = popular.get(street1);
        street2 = (String) popular.keySet().toArray()[1];
        name2 = popular.get(street2);
        street3 = (String) popular.keySet().toArray()[2];
        name3 = popular.get(street3);

        for (MessageFromTopic msg : elements) {
            stddev += Math.pow(msg.tripduration - avg, 2);
        }

        stddev = Math.sqrt(stddev / count);
        Date date = new Date();

        TripDurationStatistics res = new TripDurationStatistics(min, max, avg, stddev, street1, name1, street2, name2, street3, name3, date);
//        System.out.println("final res ---> " + res);
        out.collect(res);

    }

}

