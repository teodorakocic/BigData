package org.example;

import com.google.gson.Gson;
import org.apache.flink.api.common.serialization.DeserializationSchema;
import org.apache.flink.api.common.typeinfo.TypeInformation;

import java.io.IOException;

public class DeserializationKafka implements DeserializationSchema<MessageFromTopic> {
    private static final Gson gson = new Gson();

    @Override
    public TypeInformation<MessageFromTopic> getProducedType() {
        return TypeInformation.of(MessageFromTopic.class);
    }

    @Override
    public MessageFromTopic deserialize(byte[] arg0) throws IOException {
        MessageFromTopic res = gson.fromJson(new String(arg0), MessageFromTopic.class);
        return res;
    }

    @Override
    public boolean isEndOfStream(MessageFromTopic arg0) {
        return false;
    }

}
