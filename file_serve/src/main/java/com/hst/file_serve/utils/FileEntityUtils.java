package com.hst.file_serve.utils;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;


@Component
public class FileEntityUtils {
    public String rsl1;
    public String rsl2;
    public String rsl3;
    public String input;

    //调用线程池
    public void UseEntityThreadPool(List<String> input) {
        EntityThreadPool etp = new EntityThreadPool(input);
        etp.ThreadPool();
    }

    //调用线程
    public List<JSONObject> UseEntityThread(List<String> input) {
        EntityThread et = new EntityThread(input);
        et.startThread();
        return et.getEntityResults();
    }

    //获取实体
    public JSONObject getEntity(String input) {
        try {
            ProcessBuilder processBuilder = new ProcessBuilder("python", "D:\\Users\\17614\\PycharmProjects\\BiLSTM_CRF_NER\\predict.py", input);
            Process process = processBuilder.start();
            // 读取Python脚本输出
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), "GB2312"));
            String data = reader.readLine();

            // 读取python脚本报错，如果有
            BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream(), "GB2312"));
            String errorLine;
            while ((errorLine = errorReader.readLine()) != null) {
                System.out.println(errorLine);
            }
            String cleanedString = data.replace("'", "\"");
            System.out.println(cleanedString);
            // 将字符串转换为 JSON 对象
            JSONObject obj = JSON.parseObject(cleanedString);

            JSONArray jsonArr = new JSONArray();
            String[] tag = {"people", "time", "place", "thing", "num"};

            // 关系数据图谱化
            ArrayList<ArrayList<String>> relation_list = obj.getObject("relation", ArrayList.class);
            System.out.println(relation_list);

            List<String> exits = new ArrayList<>(); //存放已经出现过的节点名，用于检验是否重复出现
            JSONArray result_list1 = new JSONArray();//存放关系节点link的信息
            JSONArray result_list2 = new JSONArray();//存放关系节点data的信息
            int m = 0;
            JSONObject re_num = new JSONObject(); // 节点到id的索引
            for (List<String> j : relation_list) {
                for (int i = 0; i < j.size() - 2; i++) {
                    if (!exits.contains(j.get(i))) {
                        JSONObject js2 = new JSONObject();
                        js2.put("name", j.get(i));
                        js2.put("id", m);
                        js2.put("des", j.get(i));
                        result_list2.add(js2);
                        exits.add(j.get(i));
                        re_num.put(j.get(i), m);
                        m++;
                    }
                }
            }
            System.out.println(result_list2);
            System.out.println(re_num);

            for(List<String> j : relation_list){
                JSONObject js1 = new JSONObject();
                js1.put("source", re_num.getInteger(j.get(0)));
                js1.put("target", re_num.getInteger(j.get(1)));
                js1.put("value", j.get(2));
                result_list1.add(js1);
            }

            System.out.println(result_list1);

            ArrayList<ArrayList<Integer>> array = new ArrayList<>();
            int k = 0;
            for (String str : tag) {
                List<String> strings = JSON.parseArray(obj.getJSONArray(str).toString(), String.class);
                ArrayList<Integer> arr = new ArrayList<>();
                if (strings.toString().equals("[]")) {
                    JSONObject js = new JSONObject();
                    js.put("name", str.concat("为空"));
                    js.put("id", k);
                    js.put("des", str.concat("为空"));
                    jsonArr.add(js);
                    arr.add(k);
                    k++;
                } else {
                    for (String s : strings) {
                        JSONObject js = new JSONObject();
                        js.put("name", s);
                        js.put("id", k);
                        js.put("des", s);
                        jsonArr.add(js);
                        arr.add(k);
                        k++;
                    }
                }
                array.add(arr);
            }

            JSONArray jsonArray = new JSONArray();

            for (int i = 0; i < array.size() - 1; i++) {
                for (int n = 0; n < array.get(i).size(); n++) {
                    for (int j = 0; j < array.get(i + 1).size(); j++) {
                        JSONObject js = new JSONObject();
                        js.put("source", array.get(i).get(n));
                        js.put("target", array.get(i + 1).get(j));
                        js.put("value", "");
                        jsonArray.add(js);
                    }
                }
            }

            JSONObject result2 = new JSONObject();
            result2.put("result2_1", jsonArr);
            result2.put("result2_2", result_list2);

            JSONObject result3 = new JSONObject();
            result3.put("result3_1", jsonArray);
            result3.put("result3_2", result_list1);

            JSONObject result = new JSONObject();
            result.put("rsl1", obj);
            result.put("rsl2", result2);
            result.put("rsl3", result3);

            rsl1 = obj.toString();
            rsl2 = jsonArr.toString();
            rsl3 = jsonArray.toString();
            this.input = input;

            return result;
        } catch (Exception e) {
            System.out.println("getEntity出错：" + e.getMessage());
            e.printStackTrace();
            return new JSONObject();
        }
    }

    //获取实体关系
    public void getRelation(String rsl1, String input) {
        try {
            // 创建ProcessBuilder对象，设置Python脚本路径和参数
            ProcessBuilder pBuilder = new ProcessBuilder("python", "D:\\Users\\17614\\PycharmProjects\\BiLSTM_Attention\\predict_rlt.py", rsl1, input);
            // 启动进程
            Process p = pBuilder.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream(), "GB2312"));
            String data = reader.readLine();
            System.out.println(data);

            // 等待进程执行完毕
            int exitCode = p.waitFor();
            // 输出Python脚本的执行结果
            System.out.println("Python script exited with code: " + exitCode);
        } catch (Exception e) {
            System.out.println("getRelation出错：" + e.getMessage());
            e.printStackTrace();
        }
    }

    public JSONArray getInput(List<String> str) {
        JSONArray jsonArray = new JSONArray();
        for (String s : str) {
            JSONObject obj = new JSONObject();
            obj.put("input", s);
            jsonArray.add(obj);
        }
        return jsonArray;
    }

    public JSONArray getName(List<String> str) {
        JSONArray jsonArray = new JSONArray();
        for (String s : str) {
            JSONObject obj = new JSONObject();
            obj.put("name", s);
            jsonArray.add(obj);
        }
        return jsonArray;
    }
}
