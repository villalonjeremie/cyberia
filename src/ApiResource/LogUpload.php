<?php

namespace App\ApiResource;

use ApiPlatform\Metadata\ApiResource;
use ApiPlatform\Metadata\Post;
use App\State\LogUploadProcessor;

#[ApiResource(
    operations: [
        new Post(
            processor: LogUploadProcessor::class,
            deserialize: false
        )
    ]
)]
class LogUpload
{
}
