import csv
import os
import pandas as pd
import pydicom


def person_names_callback(dataset):
    dataset['PatientName'].value = "Anonymous"


def main():
    with open('tree.csv', 'w', encoding='UTF-8') as csvfile:
        directory = 'src'
        fieldnames = ['Source path', 'Output path']
        writer = csv.DictWriter(csvfile, dialect='excel', fieldnames=fieldnames)
        writer.writeheader()
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            ds = pydicom.dcmread(f, force=True)
            writer.writerow({'Source path': f,
                             'Output path': f'output\{ds["StudyInstanceUID"].value}\{ds["SeriesInstanceUID"].value}/{ds["SOPInstanceUID"].value}.dcm'})
            try:
                os.makedirs(f'output\{ds["StudyInstanceUID"].value}\{ds["SeriesInstanceUID"].value}')
                person_names_callback(ds)
            except OSError:
                print('Directory already exists.')
            except KeyError:
                print('Patient name does not exist???')
            finally:
                ds.save_as(
                    f'output\{ds["StudyInstanceUID"].value}\{ds["SeriesInstanceUID"].value}\{ds["SOPInstanceUID"].value}.dcm')
        csvfile.close()
        read_file = pd.read_csv (r'tree.csv')
        read_file.to_excel (r'tree.xlsx', index = None, header=True)
    return 0


main()
