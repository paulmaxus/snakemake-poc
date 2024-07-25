import sys
from scraper import scrape
from concurrent.futures import ThreadPoolExecutor


def get_least_common_words(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
        last_three_lines = lines[-3:]
    last_three_words = [line.split(' ')[0] for line in last_three_lines]
    return last_three_words


def define_least_common_words(input_file, output_file, threads):
    words = get_least_common_words(input_file)
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(scrape, word) for word in words]
        # execute
        definitions = [future.result() for future in futures]
    with open(output_file, 'w') as output:
        for w,d in definitions:
            if d:
                output.write(f'{w}: {d}\n')
            else:
                output.write(f'{w}: No definition found\n')


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    threads = int(sys.argv[3])
    define_least_common_words(input_file, output_file, threads)
