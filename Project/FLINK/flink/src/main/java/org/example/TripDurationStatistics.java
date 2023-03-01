package org.example;

import java.util.Date;

import com.datastax.driver.mapping.annotations.Column;
import com.datastax.driver.mapping.annotations.Table;

@Table(keyspace = "bigdata", name = "tripduration")
public class TripDurationStatistics {
    @Column(name = "max")
    public Float max;
    @Column(name = "min")
    public Float min;
    @Column(name = "avg")
    public Float avg;
    @Column(name = "stddev")
    public Double stddev;
    @Column(name = "street1")
    public String street1;
    @Column(name = "name1")
    public Integer name1;
    @Column(name = "street2")
    public String street2;
    @Column(name = "name2")
    public Integer name2;
    @Column(name = "street3")
    public String street3;
    @Column(name = "name3")
    public Integer name3;
    @Column(name = "date")
    public Date date;

    public TripDurationStatistics() {

    }

    public TripDurationStatistics(float min, float max, float avg, double stddev, String street1, int name1, String street2, int name2, String street3, int name3, Date date)
    {
        this.min = min;
        this.max = max;
        this.avg = avg;
        this.stddev = stddev;
        this.street1 = street1;
        this.name1 = name1;
        this.street2 = street2;
        this.name2 = name2;
        this.street3 = street3;
        this.name3 = name3;
        this.date = date;
    }



    @Override
    public String toString() {
        return "min: " + this.min.toString() + "max: " + this.max.toString()
                + "avg: " + this.avg.toString() + "stddev: " + this.stddev.toString() + this.street1 + ": " + this.name1.toString() + this.street2 + ": " + this.name2.toString() + this.street3 + ": " + this.name3.toString() + "date: " + this.date.toString();
    }

    public Float getMax() {
        return max;
    }

    public void setMax(Float max) {
        this.max = max;
    }

    public Float getMin() {
        return min;
    }

    public void setMin(Float min) {
        this.min = min;
    }

    public Float getAvg() {
        return avg;
    }

    public void setAvg(Float avg) {
        this.avg = avg;
    }

    public Double getStddev() {
        return stddev;
    }

    public void setStddev(Double stddev) {
        this.stddev = stddev;
    }

    public String getStreet1() {
        return street1;
    }

    public void setStreet1(String street1) {
        this.street1 = street1;
    }

    public Integer getName1() {
        return name1;
    }

    public void setName1(Integer name1) {
        this.name1 = name1;
    }

    public String getStreet2() {
        return street2;
    }

    public void setStreet2(String street2) {
        this.street2 = street2;
    }

    public Integer getName2() {
        return name2;
    }

    public void setName2(Integer name2) {
        this.name2 = name2;
    }

    public String getStreet3() {
        return street3;
    }

    public void setStreet3(String street3) {
        this.street3 = street3;
    }

    public Integer getName3() {
        return name3;
    }

    public void setName3(Integer name3) {
        this.name3 = name3;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }
}
