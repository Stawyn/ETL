import os
import json
from glob import glob

def load_data_from_file(file_path):
    with open(file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def process_folder(folder_path):
    price_variations = []
    availabilities = []
    index = 0

    json_files = glob(os.path.join(folder_path, '*.json'))
    total_files = len(json_files)

    for file_path in json_files:
        data = load_data_from_file(file_path)

        assortment = data.get('assortment', [])

        for item in assortment:
            dateTimeReference = item.get('dateTimeReference')
            idRetailerSKU = item.get('idRetailerSKU')
            priceVariation = item.get('priceVariation')

            if dateTimeReference and idRetailerSKU and priceVariation is not None:
                price_variations.append({
                    'dateTimeReference': dateTimeReference,
                    'idRetailerSKU': idRetailerSKU,
                    'priceVariation': priceVariation
                })

            available = item.get('available')
            if available is not None and available == False:
                availabilities.append({
                    'idRetailerSKU': idRetailerSKU,
                    'available': available
                })

        index += 1
        print(f'Arquivos processados {index}/{total_files}')

    top_price_variations = sorted(price_variations, key=lambda x: x['priceVariation'], reverse=True)[:10]
    top_availabilities = sorted(availabilities, key=lambda x: x['available'], reverse=True)[:10]

    return top_price_variations, top_availabilities

def main():
    folder_path = r'D:\root\workspace\data-eng-test'
    top_price_variations, top_availabilities = process_folder(folder_path)

    print('Top 10 produtos com maior variação de preço:')
    if top_price_variations:
        for product in top_price_variations:
            print(f'Data: {product["dateTimeReference"]}, ID: {product["idRetailerSKU"]}, Variação de Preço: {product["priceVariation"]}')
    else:
        print('Nenhum produto encontrado.')

    print('\nTop 10 produtos com maior indisponibilidade:')
    if top_availabilities:
        for product in top_availabilities:
            print(f'ID: {product["idRetailerSKU"]}, Disponível: {product["available"]}')
    else:
        print('Nenhum produto encontrado.')

if __name__ == '__main__':
    main()
