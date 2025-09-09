'use client';
import React, { useEffect, useState } from 'react';
import { IconBrandGithub, IconExternalLink } from '@tabler/icons-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import rehypeSanitize from 'rehype-sanitize';

export default function ContributePage() {
    const [readme, setReadme] = useState<string>('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [repoUrl, setRepoUrl] = useState<string>('');

    useEffect(() => {
        const fetchReadme = async () => {
            try {
                setLoading(true);
                setError(null);

                // Get repository path from environment variable
                const repoPathRaw = process.env.NEXT_PUBLIC_GITHUB_REPO_PATH;

                if (!repoPathRaw) {
                    throw new Error('GitHub repository path not configured');
                }

                // Extract owner/repo from full URL or use as-is if already in correct format
                let repoPath: string;
                if (repoPathRaw.includes('github.com/')) {
                    // Extract from full URL: https://github.com/owner/repo -> owner/repo
                    const match = repoPathRaw.match(/github\.com\/([^\/]+\/[^\/]+)/);
                    if (!match) {
                        throw new Error('Invalid GitHub repository URL format');
                    }
                    repoPath = match[1];
                } else {
                    // Already in owner/repo format
                    repoPath = repoPathRaw;
                }

                // Construct GitHub API URL for README
                const apiUrl = `https://api.github.com/repos/${repoPath}/readme`;
                const repoWebUrl = `https://github.com/${repoPath}`;
                setRepoUrl(repoWebUrl);

                const response = await fetch(apiUrl);

                if (!response.ok) {
                    throw new Error(`Failed to fetch README: ${response.status}`);
                }

                const data = await response.json();

                // Decode base64 content
                const readmeContent = atob(data.content);
                setReadme(readmeContent);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to load README');
                console.error('Error fetching README:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchReadme();
    }, []);

    if (loading) {
        return (
            <div className="p-4 md:p-12 pt-40 max-w-4xl mx-auto pb-32">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
                    <p className="text-muted-foreground">Loading README...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-4 md:p-12 pt-40 max-w-4xl mx-auto pb-32">
                <div className="text-center">
                    <div className="p-6 border border-red-200 rounded-lg bg-red-50 dark:bg-red-950 dark:border-red-800">
                        <h2 className="text-lg font-semibold text-red-800 dark:text-red-200 mb-2">
                            Failed to Load README
                        </h2>
                        <p className="text-red-600 dark:text-red-300 mb-4">{error}</p>
                        <p className="text-sm text-muted-foreground">
                            Please check the NEXT_PUBLIC_GITHUB_REPO_PATH environment variable.
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="p-4 md:p-12 pt-40 max-w-4xl mx-auto space-y-6 pb-32">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-semibold flex items-center gap-2">
                        <IconBrandGithub className="w-6 h-6" />
                        Contribute
                    </h1>
                    <p className="text-sm text-muted-foreground">
                        Help improve this project by contributing to the repository
                    </p>
                </div>
                {repoUrl && (
                    <a
                        href={repoUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
                    >
                        <IconBrandGithub className="w-4 h-4" />
                        View Repository
                        <IconExternalLink className="w-4 h-4" />
                    </a>
                )}
            </div>

            {/* README Content */}
            <div className="max-w-none">
                <div className="rounded-lg border bg-card p-6 prose prose-neutral dark:prose-invert prose-lg max-w-none prose-headings:text-foreground prose-p:text-foreground prose-strong:text-foreground prose-code:text-foreground">
                    <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        rehypePlugins={[rehypeRaw, rehypeSanitize]}
                        components={{
                            // Custom link component to handle relative links
                            a: ({ href, children, ...props }) => {
                                const isExternal = href?.startsWith('http') || href?.startsWith('//');
                                const finalHref = !isExternal && href?.startsWith('./')
                                    ? `${repoUrl}/blob/main/${href.slice(2)}`
                                    : !isExternal && href?.startsWith('/')
                                        ? `${repoUrl}/blob/main${href}`
                                        : href;

                                return (
                                    <a
                                        href={finalHref}
                                        target={isExternal ? "_blank" : undefined}
                                        rel={isExternal ? "noopener noreferrer" : undefined}
                                        {...props}
                                    >
                                        {children}
                                    </a>
                                );
                            },
                            // Remove all images from README
                            img: () => null,
                            // Remove picture tags from README
                            picture: () => null,
                            // Style code blocks
                            code: ({ className, children, ...props }) => {
                                return (
                                    <code
                                        className={`${className} bg-muted px-1 py-0.5 rounded text-sm font-mono`}
                                        {...props}
                                    >
                                        {children}
                                    </code>
                                );
                            },
                            pre: ({ children, ...props }) => (
                                <pre
                                    className="bg-muted p-4 rounded-lg overflow-x-auto border"
                                    {...props}
                                >
                                    {children}
                                </pre>
                            ),
                            // Handle blockquotes (like [!NOTE])
                            blockquote: ({ children, ...props }) => (
                                <blockquote
                                    className="border-l-4 border-primary pl-4 py-2 bg-muted/50 rounded-r-lg my-4"
                                    {...props}
                                >
                                    {children}
                                </blockquote>
                            ),
                            // Handle tables
                            table: ({ children, ...props }) => (
                                <div className="overflow-x-auto my-4">
                                    <table
                                        className="min-w-full border-collapse border border-border"
                                        {...props}
                                    >
                                        {children}
                                    </table>
                                </div>
                            ),
                            th: ({ children, ...props }) => (
                                <th
                                    className="border border-border bg-muted px-4 py-2 text-left font-semibold"
                                    {...props}
                                >
                                    {children}
                                </th>
                            ),
                            td: ({ children, ...props }) => (
                                <td
                                    className="border border-border px-4 py-2"
                                    {...props}
                                >
                                    {children}
                                </td>
                            ),
                            // Handle headings with better spacing
                            h1: ({ children, ...props }) => (
                                <h1
                                    className="text-3xl font-bold mt-8 mb-4 first:mt-0"
                                    {...props}
                                >
                                    {children}
                                </h1>
                            ),
                            h2: ({ children, ...props }) => (
                                <h2
                                    className="text-2xl font-semibold mt-6 mb-3 first:mt-0"
                                    {...props}
                                >
                                    {children}
                                </h2>
                            ),
                            h3: ({ children, ...props }) => (
                                <h3
                                    className="text-xl font-semibold mt-5 mb-2 first:mt-0"
                                    {...props}
                                >
                                    {children}
                                </h3>
                            ),
                            // Handle paragraphs
                            p: ({ children, ...props }) => (
                                <p
                                    className="mb-4 leading-relaxed"
                                    {...props}
                                >
                                    {children}
                                </p>
                            ),
                            // Handle lists
                            ul: ({ children, ...props }) => (
                                <ul
                                    className="list-disc list-inside mb-4 space-y-1"
                                    {...props}
                                >
                                    {children}
                                </ul>
                            ),
                            ol: ({ children, ...props }) => (
                                <ol
                                    className="list-decimal list-inside mb-4 space-y-1"
                                    {...props}
                                >
                                    {children}
                                </ol>
                            ),
                        }}
                    >
                        {readme}
                    </ReactMarkdown>
                </div>
            </div>

            {/* Footer */}
            <div className="text-center text-sm text-muted-foreground border-t pt-6">
                <p>
                    This content is automatically synced from the project's README.md file.
                    {repoUrl && (
                        <>
                            {' '}Visit the{' '}
                            <a
                                href={repoUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-primary hover:underline"
                            >
                                GitHub repository
                            </a>
                            {' '}for the latest updates.
                        </>
                    )}
                </p>
            </div>
        </div>
    );
}