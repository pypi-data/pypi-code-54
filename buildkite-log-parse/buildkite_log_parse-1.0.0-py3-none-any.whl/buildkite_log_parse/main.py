import re

from buildkite_log_parse.fetch import builds, build_job_log
from buildkite_log_parse.parser import Parser


def get_build_and_job(job_name, builds_response, build_message):
    """ Parse pipelines for active build and extract string """
    for build in builds_response:
        if re.match(build_message, build["message"]):
            for job in build["jobs"]:
                if job["name"] == job_name:
                    return build, job
    return None


def extract_job_string(job_log, regex, group=None):
    """ Extract the ssh string to connect to from log """
    matcher = re.compile(regex, re.MULTILINE)
    match = matcher.search(job_log)
    if group is not None:
        return match.group(group)
    return match.group()


def main():
    parser = Parser()
    builds_response = builds(
        parser.build_state(),
        parser.organization(),
        parser.pipeline(),
        parser.token(),
        parser.debug(),
    )
    build, job = get_build_and_job(
        parser.job(), builds_response, parser.build_message(),
    )
    log = build_job_log(
        build,
        job,
        parser.organization(),
        parser.pipeline(),
        parser.token(),
        parser.debug(),
    )
    print(extract_job_string(log, parser.regex(), parser.group()))


if __name__ == "__main__":
    main()
