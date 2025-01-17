# -*- coding: utf-8 -*-
import asyncio
import json
import os

import pytest
import responses

from pulselistener.lib.bus import MessageBus
from pulselistener.listener import CodeCoverage

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


def test_is_coverage_task(mock_taskcluster):
    bus = MessageBus()
    hook = CodeCoverage({
      'hookId': 'services-staging-codecoverage/bot'
    }, bus)

    cov_task = {
        'task': {
            'metadata': {
                'name': 'build-linux64-ccov'
            }
        }
    }
    assert hook.is_coverage_task(cov_task)

    cov_task = {
        'task': {
            'metadata': {
                'name': 'build-linux64-ccov/opt'
            }
        }
    }
    assert hook.is_coverage_task(cov_task)

    cov_task = {
        'task': {
            'metadata': {
                'name': 'build-win64-ccov/debug'
            }
        }
    }
    assert hook.is_coverage_task(cov_task)

    nocov_task = {
        'task': {
            'metadata': {
                'name': 'test-linux64-ccov/opt-mochitest-1'
            }
        }
    }
    assert not hook.is_coverage_task(nocov_task)

    nocov_task = {
        'task': {
            'metadata': {
                'name': 'test-linux64/opt-mochitest-1'
            }
        }
    }
    assert not hook.is_coverage_task(nocov_task)


@pytest.mark.asyncio
async def test_get_build_task_in_group(mock_taskcluster):
    bus = MessageBus()
    hook = CodeCoverage({
      'hookId': 'services-staging-codecoverage/bot'
    }, bus)

    hook.triggered_groups.add('already-triggered-group')

    assert await hook.get_build_task_in_group('already-triggered-group') is None


@pytest.mark.asyncio
async def test_parse(mock_taskcluster):
    bus = MessageBus()
    hook = CodeCoverage({
      'hookId': 'services-staging-codecoverage/bot'
    }, bus)

    hook.triggered_groups.add('already-triggered-group')

    assert await hook.parse({
        'taskGroupId': 'already-triggered-group'
    }) is None


def run_async_parser(hook, group_id):
    '''
    Helper to run the asynchronous parser using responses in the same event loop
    '''
    async def _check():
        with open(os.path.join(FIXTURES_DIR, f'{group_id}.json')) as f:
            responses.add(
                responses.GET,
                f'http://taskcluster.test/queue/v1/task-group/{group_id}/list',
                json=json.load(f),
                status=200,
            )
        return await hook.parse({
            'taskGroupId': group_id,
        })

    loop = asyncio.new_event_loop()
    return loop.run_until_complete(_check())


@responses.activate
def test_wrong_branch(mock_taskcluster):
    bus = MessageBus()
    hook = CodeCoverage({
      'hookId': 'services-staging-codecoverage/bot'
    }, bus)

    assert run_async_parser(hook, 'bNq-VIT-Q12o6nXcaUmYNQ') is None


@responses.activate
def test_success(mock_taskcluster):
    bus = MessageBus()
    hook = CodeCoverage({
      'hookId': 'services-staging-codecoverage/bot'
    }, bus)

    assert run_async_parser(hook, 'RS0UwZahQ_qAcdZzEb_Y9g') == [
        {'REPOSITORY': 'https://hg.mozilla.org/mozilla-central', 'REVISION': 'ec3dd3ee2ae4b3a63529a912816a110e925eb2d0'}
    ]


@responses.activate
def test_success_windows(mock_taskcluster):
    bus = MessageBus()
    hook = CodeCoverage({
      'hookId': 'services-staging-codecoverage/bot'
    }, bus)

    assert run_async_parser(hook, 'MibGDsa4Q7uFNzDf7EV6nw') == [
        {'REPOSITORY': 'https://hg.mozilla.org/mozilla-central', 'REVISION': '63519bfd42ee379f597c0357af2e712ec3cd9f50'}
    ]


@responses.activate
def test_success_try(mock_taskcluster):
    bus = MessageBus()
    hook = CodeCoverage({
      'hookId': 'services-staging-codecoverage/bot'
    }, bus)

    assert run_async_parser(hook, 'FG3goVnCQfif8ZEOaM_4IA') == [
        {'REPOSITORY': 'https://hg.mozilla.org/try', 'REVISION': '066cb18ba95a7efe144e729713c429e422d9f95b'}
    ]


def test_hook_group(mock_taskcluster):
    bus = MessageBus()
    hook = CodeCoverage({
      'hookId': 'services-staging-codecoverage/bot'
    }, bus)
    assert hook.group_id == 'project-releng'
    assert hook.hook_id == 'services-staging-codecoverage/bot'

    hook = CodeCoverage({
      'hookGroupId': 'anotherProject',
      'hookId': 'anotherHook',
    }, bus)
    assert hook.group_id == 'anotherProject'
    assert hook.hook_id == 'anotherHook'
