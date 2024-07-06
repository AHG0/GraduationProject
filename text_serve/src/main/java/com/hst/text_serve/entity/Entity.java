package com.hst.text_serve.entity;

import lombok.Data;
import org.springframework.context.annotation.Bean;

@Data
public class Entity {
    private Integer id;
    private String input;
    private String rsl1;
    private String rsl2;
    private String rsl3;
    private int userid;
}
