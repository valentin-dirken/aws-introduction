## DynamoDB Structure

TABLE NAME : vdirken_instagram

| **Attribute Name** | **Data Type** | **Description**       |
|--------------------|---------------|-----------------------|
| `publicationID`    | `String`      | !!! PARTITION KEY !!!! Unique identifier for the publication |
| `caption`          | `String`      | Description or caption for the publication |
| `location`         | `String`      | Location related to the publication |
| `imageFilename`    | `String`      | Filename of the associated image    |
| `timestamp`        | `String`      | Time when the publication was created (Unix timestamp) |
