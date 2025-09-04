import React from 'react';
import { ExternalLink, Calendar, Users, Tag, Quote } from 'lucide-react';
import { Paper } from '../types/api';

interface PaperCardProps {
  paper: Paper;
}

const PaperCard: React.FC<PaperCardProps> = ({ paper }) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const getSourceColor = (source: string) => {
    const colors = {
      arxiv: 'bg-red-100 text-red-800',
      openalex: 'bg-blue-100 text-blue-800',
      crossref: 'bg-green-100 text-green-800',
    };
    return colors[source as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  const truncateAbstract = (abstract: string, maxLength: number = 300) => {
    if (abstract.length <= maxLength) return abstract;
    return abstract.substring(0, maxLength) + '...';
  };

  return (
    <div className="paper-card">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center gap-2">
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSourceColor(paper.source)}`}>
            {paper.source_name}
          </span>
          {paper.citation_count !== undefined && paper.citation_count > 0 && (
            <span className="text-xs text-gray-500 flex items-center gap-1">
              <Quote size={12} />
              {paper.citation_count} citations
            </span>
          )}
        </div>
        <a
          href={paper.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-gray-400 hover:text-primary-600 transition-colors"
          title="View paper"
        >
          <ExternalLink size={18} />
        </a>
      </div>

      {/* Title */}
      <h3 className="text-xl font-semibold text-gray-900 mb-3 leading-tight">
        <a
          href={paper.url}
          target="_blank"
          rel="noopener noreferrer"
          className="hover:text-primary-600 transition-colors"
        >
          {paper.title}
        </a>
      </h3>

      {/* Authors and Date */}
      <div className="flex items-center gap-4 mb-3 text-sm text-gray-600">
        <div className="flex items-center gap-1">
          <Users size={14} />
          <span>{paper.formatted_authors}</span>
        </div>
        <div className="flex items-center gap-1">
          <Calendar size={14} />
          <span>{formatDate(paper.published_date)}</span>
        </div>
      </div>

      {/* Abstract */}
      <p className="text-gray-700 mb-4 leading-relaxed">
        {truncateAbstract(paper.abstract)}
      </p>

      {/* Categories */}
      {paper.categories && paper.categories.length > 0 && (
        <div className="flex items-start gap-2 mb-4">
          <Tag size={14} className="text-gray-400 mt-1 flex-shrink-0" />
          <div className="flex flex-wrap gap-1">
            {paper.categories.slice(0, 5).map((category, index) => (
              <span
                key={index}
                className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-md"
              >
                {category}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="flex justify-between items-center pt-4 border-t border-gray-100">
        <div className="text-xs text-gray-500">
          {paper.doi && (
            <span>DOI: {paper.doi}</span>
          )}
        </div>
        <a
          href={paper.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm text-primary-600 hover:text-primary-700 font-medium"
        >
          Read Paper →
        </a>
      </div>
    </div>
  );
};

export default PaperCard;
