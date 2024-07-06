package com.hst.text_serve.utils;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.*;

@Component
@Slf4j
public class Utils {
    public String classifyRsl;
    public String simiRsl;
    public String similarOne;
    public String similarTwo;
    public String similarThree;
    public String inputClassify;
    public String rsl1;
    public String rsl2;
    public String rsl3;
    public String input;
    public String inputEntity;

    public String PythonClassify(String inputData) {
        System.out.println("开始调用PythonClassify");
        try {
            ProcessBuilder processBuilder = new ProcessBuilder("python", "D:\\Users\\17614\\PycharmProjects\\pythonProject\\Python\\AILawSystem\\fen_lei\\question_classify.py ", inputData);
            Process process = processBuilder.start();
            // 读取Python脚本输出
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), "GB2312"));
            String data;
            String classifyResult = null;
            int count = 0;
            while ((data = reader.readLine()) != null) {
                System.out.println(data);
                if (count == 3) {
                    classifyResult = data;
                }
                count++;
            }

            // 读取python脚本报错，如果有
            BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream(), "GB2312"));
            String errorLine;
            while ((errorLine = errorReader.readLine()) != null) {
                System.out.println(errorLine);
            }

            System.out.println("classify_result：" + classifyResult);

            return classifyResult;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public String PythonSimilar(String inputData) {
        System.out.println("开始调用PythonSimilar");
        try {
            ProcessBuilder processBuilder = new ProcessBuilder("python", "D:\\Users\\17614\\PycharmProjects\\pythonProject\\Python\\AILawSystem\\xiang_si\\Text_Similarity.py ", inputData);
            Process process = processBuilder.start();
            // 读取Python脚本输出
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), "GB2312"));
            String similarResult = reader.readLine();

            // 读取python脚本报错，如果有
            BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream(), "GB2312"));
            String errorLine;
            while ((errorLine = errorReader.readLine()) != null) {
                System.out.println(errorLine);
            }

            System.out.println("similar_result：" + similarResult);
            return similarResult;
        } catch (Exception e) {
            System.out.println("getSimilar出错：" + e.getMessage());
            e.printStackTrace();
        }
        return null;
    }

    public JSONObject getClassify(String input) {
        System.out.println(input);
        ClassifyThread ct = new ClassifyThread(input);
        SimiThread st = new SimiThread(input);
        ct.start();
        st.start();
        try {
            ct.join();    //main方法里面调用join()方法，主线程会阻塞，等待thread1线程完成
            st.join();    //main方法里面调用join()方法，主线程会阻塞，等待thread2线程完成
        } catch (Exception e) {
            e.printStackTrace();
            return new JSONObject();
        }
        classifyRsl = ct.ClassResult;
        simiRsl = st.SimiResult;
        ArrayList<String> similarObject = new ArrayList<>();
        JSONObject clasObj = new JSONObject();
        String[] arr1 = simiRsl.split(",");
        Collections.addAll(similarObject, arr1);
        clasObj.put("classify_result", classifyRsl);
        clasObj.put("other", "缴纳满一年的是可以办理报销的。生育保险待遇由用人单位在职工产后或手术后18个月内，向社会保险经办机构申请办理，申办时应填报《职工生育待遇申领表》，并提供以下资料：计划生育行政部门核发的生育证明；生育医疗证明、门诊病历、出院小结、计划生育手术记录等原始材料；婴儿出生证。社会保险经办机构应当自受理申请之日起 15 个工作日内对用人单位提供的资料进行审核，审核完成后将生育保险费用拨付给职工所在用人单位，并由用人单位按照本办法规定的生育保险待遇项目和标准发给职工。");
        clasObj.put("similar_result", new HashMap<String, String>() {
            {
                put("similar_result_one", similarObject.get(0));
                put("similar_result_two", similarObject.get(1));
                put("similar_result_three", similarObject.get(2));
            }
        });
        similarOne = similarObject.get(0);
        similarTwo = similarObject.get(1);
        similarThree = similarObject.get(2);
        inputClassify = input;
        System.out.println("the_data：" + clasObj);
        return clasObj;
    }


    public JSONObject getEntity(String input) {
        try {
            System.out.println(input);
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

    public JSONArray getInput(List<String> str) {
        JSONArray jsonArray = new JSONArray();
        for (String s : str) {
            JSONObject obj = new JSONObject();
            obj.put("input", s);
            jsonArray.add(obj);
        }
        return jsonArray;
    }
}


