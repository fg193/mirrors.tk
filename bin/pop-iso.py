#!/usr/bin/env python3

import collections
import requests
import zeep


BUCKET = "https://pop-iso.sfo2.cdn.digitaloceanspaces.com"
WSDL = "https://doc.s3.amazonaws.com/2006-03-01/AmazonS3.wsdl"
SCHEMA = zeep.xsd.Schema(settings=zeep.Settings(strict=False))


def list_bucket():
    result_type = None
    page = dict(IsTruncated=True, NextMarker="")
    page = collections.namedtuple("ListBucketResult", page.keys())(**page)

    while page.IsTruncated:
        resp = requests.get(BUCKET, dict(marker=page.NextMarker))
        bucket = zeep.loader.parse_xml(resp.content, zeep.Transport)

        # fix the order of <Marker> and <NextMarker> in the sequence
        # https://github.com/mvantellingen/python-zeep/issues/487
        if not result_type:
            result_type = zeep.Client(WSDL).get_type(bucket.tag)
            key, seq = result_type.elements_nested[0]
            seq = zeep.xsd.Sequence(seq[:3] + seq[5:] + seq[3:5])
            result_type.elements_nested = [(key, seq)]

        page = result_type.parse_xmlelement(bucket, SCHEMA)
        yield from page.Contents


if __name__ == "__main__":
    for obj in list_bucket():
        print("#", obj.LastModified.timestamp(), obj.Size)
        print(obj.Key)
