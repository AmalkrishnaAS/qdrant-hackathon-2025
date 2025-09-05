
import { IconMusic, IconChevronRight } from "@tabler/icons-react";
import Upload from "@/components/home/upload";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AudioCropper } from "@/components/home/audio-crop";

export default function Home() {
  const items = [
    {
      title: "All of Me",
      category: "John Lennon",
      description: "",
      link: "#",
      icon: <IconMusic className="h-full text-neutral-500 dark:text-neutral-300" />,
    },
    {
      title: "All of Me",
      category: "John Lennon",
      description: "",
      link: "#",
      icon: <IconMusic className="h-full text-neutral-500 dark:text-neutral-300" />,
    },
    {
      title: "All of Me",
      category: "John Lennon",
      description: "",
      link: "#",
      icon: <IconMusic className="h-full text-neutral-500 dark:text-neutral-300" />,
    },
    {
      title: "All of Me",
      category: "John Lennon",
      description: "",
      link: "#",
      icon: <IconMusic className="h-full text-neutral-500 dark:text-neutral-300" />,
    },
    {
      title: "All of Me",
      category: "John Lennon",
      description: "",
      link: "#",
      icon: <IconMusic className="h-full text-neutral-500 dark:text-neutral-300" />,
    },
    {
      title: "All of Me",
      category: "John Lennon",
      description: "",
      link: "#",
      icon: <IconMusic className="h-full text-neutral-500 dark:text-neutral-300" />,
    },
    {
      title: "All of Me",
      category: "John Lennon",
      description: "",
      link: "#",
      icon: <IconMusic className="h-full text-neutral-500 dark:text-neutral-300" />,
    },
    {
      title: "All of Me",
      category: "John Lennon",
      description: "",
      link: "#",
      icon: <IconMusic className="h-full text-neutral-500 dark:text-neutral-300" />,
    },
    {
      title: "All of Me",
      category: "John Lennon",
      description: "",
      link: "#",
      icon: <IconMusic className="h-full text-neutral-500 dark:text-neutral-300" />,
    },
  ];

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-7xl mx-auto mt-20 sm:mt-6">
        <Tabs defaultValue="upload" className="w-full">
          <TabsList className="grid w-full grid-cols-3 max-w-lg mx-auto">
            <TabsTrigger value="upload" className="flex items-center gap-1">
              Upload <IconChevronRight className="h-4 w-4" />
            </TabsTrigger>
            <TabsTrigger value="edit" className="flex items-center gap-1">
              Edit <IconChevronRight className="h-4 w-4" />
            </TabsTrigger>
            <TabsTrigger value="download" className="flex items-center gap-1">
              Download <IconChevronRight className="h-4 w-4" />
            </TabsTrigger>
          </TabsList>
          <TabsContent value="upload" className="mt-6">
            <Upload items={items} />
          </TabsContent>
          <TabsContent value="edit" className="mt-6">
            <AudioCropper />
          </TabsContent>
          <TabsContent value="download" className="mt-6">
            <div className="text-center py-8">
              <h3 className="text-lg font-medium">Download Content</h3>
              <p className="text-muted-foreground mt-2">Download your files here</p>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
