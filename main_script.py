import csv
import os
import pandas as pd
import pydicom


def person_names_callback(dataset):
    """person anonymize"""
    dataset['PatientName'].value = "Anonymous"


def main() -> None:
    """file refactoring"""
    with open('tree.csv', 'w', encoding='UTF-8') as csvfile:
        directory = 'src'
        fieldnames = ['Source path', 'Output path']
        writer = csv.DictWriter(csvfile, dialect='excel', fieldnames=fieldnames)
        writer.writeheader()
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            dicom_data = pydicom.dcmread(file_path, force=True)
            writer.writerow({'Source path': file_path,
                             'Output path': f'output/{dicom_data["StudyInstanceUID"].value}/'
                                            f'{dicom_data["SeriesInstanceUID"].value}/'
                                            f'{dicom_data["SOPInstanceUID"].value}.dcm'})
            try:
                os.makedirs(f'output/{dicom_data["StudyInstanceUID"].value}/'
                            f'{dicom_data["SeriesInstanceUID"].value}')
                person_names_callback(dicom_data)
            except OSError:
                print('Directory already exists.')
            except KeyError:
                print('Patient name does not exist???')
            finally:
                dicom_data.save_as(
                    f'output/{dicom_data["StudyInstanceUID"].value}/'
                    f'{dicom_data["SeriesInstanceUID"].value}/'
                    f'{dicom_data["SOPInstanceUID"].value}.dcm')
        csvfile.close()
        read_file = pd.read_csv(r'tree.csv')
        read_file.to_excel(r'tree.xlsx', index=None, header=True)

if __name__ == '__main__':
    main()
