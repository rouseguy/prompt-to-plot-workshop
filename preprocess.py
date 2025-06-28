import csv, json, random, math, os, statistics

SOURCE = 'GoodReads_100k_books.csv'
OUT = 'scatter_data.json'
SAMPLE_SIZE = 5000
SEED = 42

rows = []
pages_vals = []
blurb_vals = []
reviews_vals = []
rating_vals = []

with open(SOURCE, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    reader.fieldnames = [h.lstrip('\ufeff') for h in reader.fieldnames]
    for r in reader:
        try:
            pages = int(r['pages']) if r['pages'] else None
            reviews = int(r['reviews']) if r['reviews'] else None
            rating = float(r['rating']) if r['rating'] else None
            desc = r['desc'] or ''
        except KeyError:
            continue
        if pages is None or reviews is None or rating is None:
            continue
        blurb = len(desc)
        row = {'pages': pages, 'blurb': blurb, 'reviews': reviews, 'rating': rating}
        rows.append(row)
        pages_vals.append(pages)
        blurb_vals.append(blurb)
        reviews_vals.append(reviews)
        rating_vals.append(rating)


def percentile(values, pct):
    s = sorted(values)
    k = (len(s) - 1) * pct / 100.0
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return s[int(k)]
    d0 = s[f] * (c - k)
    d1 = s[c] * (k - f)
    return d0 + d1

limits = {}
for name, vals in [('pages', pages_vals), ('blurb', blurb_vals), ('reviews', reviews_vals), ('rating', rating_vals)]:
    low = percentile(vals, 0.5)
    high = percentile(vals, 99.5)
    limits[name] = (low, high)

filtered = [r for r in rows if
            limits['pages'][0] <= r['pages'] <= limits['pages'][1] and
            limits['blurb'][0] <= r['blurb'] <= limits['blurb'][1] and
            limits['reviews'][0] <= r['reviews'] <= limits['reviews'][1] and
            limits['rating'][0] <= r['rating'] <= limits['rating'][1]]

random.seed(SEED)
if len(filtered) > SAMPLE_SIZE:
    filtered = random.sample(filtered, SAMPLE_SIZE)

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(filtered, f, separators=(',', ':'))

size = os.path.getsize(OUT)
print(size)
