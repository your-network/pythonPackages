def processWorkerAlive(workers, worker, subscriber, subscription_path):
    import os

    ack_ids, renew_count, worker_num = workers[worker]
    # should renew the ack window now
    subscriber.modify_ack_deadline(
        subscription_path,
        [ack_ids],
        ack_deadline_seconds = int(os.environ['ACK_DEADLINE_SECONDS'])
    )

    print(f"renewing the ack window for msgs {ack_ids} for {renew_count} renew count with worker {worker_num}")
    renew_count += 1
    workers[worker] = (ack_ids, renew_count, worker_num)