<?php

namespace App\State;

use ApiPlatform\Metadata\Operation;
use ApiPlatform\State\ProcessorInterface;
use Symfony\Component\HttpFoundation\RequestStack;
use Symfony\Component\HttpFoundation\File\UploadedFile;
use Symfony\Component\HttpFoundation\JsonResponse;

final class LogUploadProcessor implements ProcessorInterface
{
    public function __construct(
        private RequestStack $requestStack
    ) {}

    public function process(
        mixed $data,
        Operation $operation,
        array $uriVariables = [],
        array $context = []
    ) {
        $request = $this->requestStack->getCurrentRequest();

        if (!$request) {
            throw new \RuntimeException('Request introuvable');
        }

        /** @var UploadedFile|null $file */
        $file = $request->files->get('file');

        if (!$file instanceof UploadedFile) {
            throw new \RuntimeException('Aucun fichier reçu');
        }

        if ($file->getClientOriginalExtension() !== 'log') {
            throw new \RuntimeException('Extension non autorisée');
        }

        $content = file_get_contents($file->getPathname());
        $lines = preg_split("/\R/", trim($content));

        return new JsonResponse([
            'filename' => $file->getClientOriginalName(),
            'linesCount' => count($lines),
        ]);
    }
}
