<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\JsonResponse;


class LogUploadController extends AbstractController
{
    #[Route('/api/upload-log', name: 'upload_log', methods: ['POST'])]
    public function upload(Request $request): Response
    {
        $lines = [];

        if ($request->isMethod('POST')) {
            $file = $request->files->get('file');

            if ($file && $file->getClientOriginalExtension() === 'log') {
                $lines = file($file->getPathname(), FILE_IGNORE_NEW_LINES);
            }
        }

        return new JsonResponse([
            'lines' => $lines,
            'count' => count($lines),
        ]);
    }
}
