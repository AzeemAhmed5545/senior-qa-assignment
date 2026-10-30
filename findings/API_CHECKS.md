# API Checks (§2)

| Item     | Detail                                                                     |
| -------- | -------------------------------------------------------------------------- |
| Endpoint | `POST https://automationexercise.com/api/searchProduct` (`search_product`) |
| Docs     | [api_list](https://automationexercise.com/api_list) — API 5 and API 6      |
| Tools    | Postman + curl · 30 Oct                                                    |

## Results

| ID  | Request                          | HTTP    | Body code | Body                                    | Docs say      | Result              |
| --- | -------------------------------- | ------- | --------- | --------------------------------------- | ------------- | ------------------- |
| A1  | `search_product=top`             | 200     | 200       | 14 products, Blue Top Rs. 500           | 200 + list    | ✅ PASS             |
| A2  | `search_product=zzzznotfound123` | 200     | 200       | `"products": []`                        | not described | ✅ PASS             |
| A3  | parameter missing                | **200** | **400**   | "search_product parameter is missing…"  | 400 + message | ✅ body · ⚠️ AMB-01 |
| A4  | blank value _(extra)_            | 200     | 200       | all 34 products                         | not described | Observation         |
| A5  | `GET` _(extra)_                  | 200     | 405       | "This request method is not supported." | POST only     | ✅ PASS             |
| A6  | `other=x` _(extra)_              | 200     | 400       | same as A3                              | 400           | ✅ body · ⚠️ AMB-01 |

**Confirmed API defects: none.** Every body matches the docs.

## Open question — AMB-01

The docs say **"Response Code: 400"** but not whether that is the **HTTP status** or the **body
field**.

| If the docs mean… | Then                                                  |
| ----------------- | ----------------------------------------------------- |
| HTTP status       | Defect — clients and monitoring see errors as success |
| Body field        | Works as documented — docs should say so              |

Needs the API owner to confirm. Suggestion: IMP-04.

## Observations (not defects)

| ID     | Seen                                                           | Note   |
| ------ | -------------------------------------------------------------- | ------ |
| OBS-01 | JSON sent as `Content-Type: text/html`                         | IMP-04 |
| OBS-02 | Blank search returns all 34 products                           | IMP-05 |
| OBS-03 | 2 of 14 "top" results match on category, not name (ids 18, 24) | IMP-03 |

## Evidence (`evidence/api/`)

| Case    | Postman screenshot                  | Test results                                    | Raw response (curl)         |
| ------- | ----------------------------------- | ----------------------------------------------- | --------------------------- |
| A1 – A6 | `postman-A1.png` … `postman-A6.png` | `postman-A1-tests.png` … `postman-A6-tests.png` | `A1-raw.txt` … `A6-raw.txt` |

## Repeat it

**Postman:** Import `api/AutomationExercise-SearchProduct.postman_collection.json` → Run (18 tests).

**curl:**

```
curl -s -i -X POST -d "search_product=top" https://automationexercise.com/api/searchProduct
curl -s -i -X POST -d "search_product=zzzznotfound123" https://automationexercise.com/api/searchProduct
curl -s -i -X POST https://automationexercise.com/api/searchProduct
```
