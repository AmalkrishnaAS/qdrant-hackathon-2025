import { FileUpload } from "@/components/ui/file-upload";
import { List2 } from "@/components/ui/list";
import { IconMusic } from "@tabler/icons-react";

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
  ];
  return (
    <div className="min-h-screen flex items-center p-4 md:p-8">
      <div className="container mx-auto grid md:grid-cols-2 gap-8">
        <div className="flex items-center justify-center">
          <div className="w-full max-w-md">
            <FileUpload />
          </div>
        </div>
        <div className="max-h-[70vh] overflow-y-auto pr-4">
          <List2
          heading={`Recommended Tracks (${items.length})`}
          items={items}
          />
        </div>
      </div>
    </div>
  );
}
