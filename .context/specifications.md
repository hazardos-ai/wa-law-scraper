# Specifications

## Goal

Extract all title, chapter, and section while maintaining knowledge connections for creating both a relational and graph database implementation. After this, APIs will be created for structuring and validating data input and output.

## State of Washington legal code information

There are 2 types of Washington State laws:
- Washington Administrative Code (WAC) are regulations of executive branch agencies are issued by authority of statutes. Like legislation and the Constitution, regulations are a source of primary law in Washington State. The WAC codifies the regulations and arranges them by subject or agency.
  - Base URL: https://app.leg.wa.gov/wac/default.aspx
- The Revised Code of Washington (RCW) is the compilation of all permanent laws now in force. It is a collection of Session Laws (enacted by the Legislature, and signed by the Governor, or enacted via the initiative process), arranged by topic, with amendments added and repealed laws removed. It does not include temporary laws such as appropriations acts.
  - Base URL: https://app.leg.wa.gov/RCW/default.aspx
The two types of legal codes have different base urls but have identical site structure
