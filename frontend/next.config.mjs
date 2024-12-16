/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "standalone",
    images: {
        remotePatterns: [
            {
                protocol: 'https',
                hostname: 'assets.aceternity.com',
                pathname: '**'
            },
            {
                protocol: 'https',
                hostname: 'nextui.org',
                pathname: '**'
            },
            {
                protocol: 'https',
                hostname: 'i.ytimg.com',
                pathname: '**'
            }
        ]
    }
};

export default nextConfig;
