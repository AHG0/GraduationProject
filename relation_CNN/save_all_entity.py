import json

exist = []


def extract_relations_to_txt(json_line, txt_file):
    json_data = json.loads(json_line)
    relations = json_data["relationMentions"]

    for relation in relations:
        entity1 = relation["em1Text"]
        entity2 = relation["em2Text"]
        if entity1 not in exist:
            txt_file.write(entity1 + '\n')
            exist.append(entity1)
        if entity2 not in exist:
            txt_file.write(entity2 + '\n')
            exist.append(entity2)


def process_json_file(json_filename, txt_filename):
    with open(json_filename, 'r', encoding='utf-8') as jsonfile, \
            open(txt_filename, 'w', encoding='utf-8') as txtfile:
        for json_line in jsonfile:
            # Extract labels from each line of the JSON file
            extract_relations_to_txt(json_line, txtfile)


if __name__ == '__main__':
    # Specify the input JSON filename and the output TXT filename
    json_filename = r'D:\Users\17614\PycharmProjects\relation_CNN\orig_data\step1_train.json'
    txt_filename = r'D:\Users\17614\PycharmProjects\relation_CNN\all_labels.txt'

    # Process the JSON file and write labels to TXT
    process_json_file(json_filename, txt_filename)
